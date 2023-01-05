import base64
import io
import time
import datetime
import logging
import uuid

import pika
from pika import exceptions as pika_exceptions
import json
import os
from typing import List
import sqlalchemy
import datetime
from core import settings
from fastapi import UploadFile
from . import request
from sqlalchemy import column, desc

from db.models import AutoMLTask, NodelRole, \
    MLTaskStatus, AutoMLReceiveMessage, MessageConsumeStatus, FedCalculationNetworkNode, FedCalculationTaskNode, FedLog, \
    FedReceiveMessage, AppStatus
from sqlalchemy.ext.asyncio import AsyncSession
from core.settings import COS_SETTINGS
from libs.cos_client import CosTools
from db.models import TaskType, MLTaskStatus, TaskStatus

_logger = logging.getLogger("app")


async def create_task_db(db: AsyncSession, data: request.TaskCreateModel, db_task: AutoMLTask = None) -> (
        AutoMLTask, str):
    try:
        async with db:
            if data.current_node == data.publish_node:
                node_list = [{"node_id": data.current_node, "status": MLTaskStatus.JOIN_NETWORK.value}]
            else:
                node_list = [{"node_id": data.current_node, "status": 0},
                             {"node_id": data.publish_node, "status": MLTaskStatus.JOIN_NETWORK.value},
                             ]

            insert_dict = {
                "create_at": datetime.datetime.now(),
                "update_at": datetime.datetime.now(),
                "created_by": "system",
                "task_id": data.task_id,
                "task_name": data.task_name,
                "description": data.description,
                "dataset_id": data.dataset_id,
                "dataset_version": data.dataset_version,
                "model_name": data.model_name,
                "model_id": data.model_id,
                "node_list": node_list,
                "calculation_type": data.calculation_type,
                "initiator_node": data.publish_node,
                "current_node_role": NodelRole.INITIATOR if data.publish_node == data.current_node else NodelRole.PARTICIPANT,
                'status': MLTaskStatus.INIT,
                'report': None,
                'result_model': None,
                'start_time': None,
                'end_time': None,
                'calculation_time': 0,
                'forecast_calculation_time': 0,
                'dataset_meta': None, 'model_local_file': None, 'model_meta': None,
                "message": "",
                "progress_number": 0,
                "pid": -1,
            }
            if db_task:
                for key, value in insert_dict.items():
                    setattr(db_task, key, value)
                db_task = await db.merge(db_task)
            else:
                db_task = AutoMLTask(**insert_dict)

            db.add(db_task)
            await db.commit()
            await db.refresh(db_task)
            return db_task, ""
    except sqlalchemy.exc.IntegrityError as e:
        _logger.exception(e)
        return None, e.__repr__()


async def get_task_detail(db: AsyncSession, task_id: str) -> (dict, str):
    try:
        async with db:
            select_sql = sqlalchemy.select(AutoMLTask).filter(AutoMLTask.task_id == task_id.strip())
            task_obj: AutoMLTask = (await db.execute(select_sql)).scalar_one_or_none()
            assert task_obj, f"get task detail failed by {task_id}"
            return task_obj.to_dict(), ""
    except AssertionError as e:
        return {}, str(e)


async def get_task_list(db: AsyncSession) -> (list, str):
    try:
        async with db:
            select_sql = sqlalchemy.select(AutoMLTask).filter(AutoMLTask.initiator_node == os.environ.get("NODE_ID"))
            task_scalars = await db.execute(select_sql)
            return [line.to_dict() for line in task_scalars.scalars()], ""
    except AssertionError as e:
        return [], str(e)


async def start_task(db: AsyncSession, data: request.TaskStartModel) -> (bool, str):
    """
    检查本地的节点加入状态,如果有节点离线【报错】尝试通知一次加入计算 notify_add_network
    如果所有节点均加入计算，则开始执行计算的流程
    1. 检查节点状态
    2. 检查
    """
    try:
        async with db:
            select_sql = sqlalchemy.select(AutoMLTask).filter(AutoMLTask.task_id == data.task_id.strip())
            task_obj: AutoMLTask = (await db.execute(select_sql)).scalar_one_or_none()
            assert task_obj, f"get task failed by {data.task_id}"
            db_node_list = task_obj.node_list
            db_node_id_list = sorted([x.get("node_id") for x in db_node_list])
            data.node_list.sort()

            if db_node_id_list != data.node_list:
                new_node_list = []
                for item in data.node_list:
                    new_node_list.append({
                        "node_id": item,
                        "status": MLTaskStatus.JOIN_NETWORK.value
                    })
                task_obj.update_at = datetime.datetime.now()
                task_obj.node_list = new_node_list
                task_obj = await db.merge(task_obj)
                db.add(task_obj)
                await db.commit()
        _logger.info("start push message to runtime")
        call_node_list = [item.get("node_id") for item in task_obj.node_list]
        message_dict = {
            "task_id": data.task_id,
            "node_id_list": call_node_list,
            "message_title": "task_start_running",
            "message_time": int(time.time()),
            "message_content": {
                "task_id": data.task_id,
                "time": int(time.time()),
                "event": "task_start_running"
            },
        }
        await push_message(message_dict)
        return True, ""
    except Exception as e:
        return False, str(e)


async def restart_task(db: AsyncSession, data: request.TaskIdModel) -> (bool, str):
    """
    发送重启任务的消息
    """
    try:
        async with db:
            select_sql = sqlalchemy.select(AutoMLTask).filter(AutoMLTask.task_id == data.task_id.strip())
            task_obj: AutoMLTask = (await db.execute(select_sql)).scalar_one_or_none()
            assert task_obj, f"get task failed by {data.task_id}"

        if task_obj.status not in (
                MLTaskStatus.START, MLTaskStatus.RESULT_UPLOAD, MLTaskStatus.FINISHED,
                MLTaskStatus.RUNNING_START_ERROR, MLTaskStatus.UPLOAD_ERROR, MLTaskStatus.FINISH_ERROR,
                MLTaskStatus.KILL_ERROR, MLTaskStatus.UPLOAD_ERROR):
            _logger.warning(f"task is not ready status {task_obj.status.name}")
            return False, f"只有启动或者运行失败的任务才可以重启: {task_obj.status.name}"

        _logger.info("start push restart message to runtime")
        call_node_list = [item.get("node_id") for item in task_obj.node_list]
        message_dict = {
            "task_id": data.task_id,
            "node_id_list": call_node_list,
            "message_title": "task_restart",
            "message_time": int(time.time()),
            "message_content": {
                "task_id": data.task_id,
                "time": int(time.time()),
                "event": "task_restart"
            },
        }
        await push_message(message_dict)
        return True, ""
    except AssertionError as e:
        return False, str(e)


async def delete_task(db: AsyncSession, data: request.TaskIdModel) -> (bool, str):
    """
    删除任务.
    1. 停止正在运行的进程
    2. 删除运行中产生的文件夹等
    3. 删除任务日志数据表
    4. 删除任务消息数据表
    5. 删除任务数据表?
    """
    try:
        async with db:
            select_sql = sqlalchemy.select(AutoMLTask).filter(AutoMLTask.task_id == data.task_id.strip())
            task_obj: AutoMLTask = (await db.execute(select_sql)).scalar_one_or_none()
            assert task_obj, f"get task failed by {data.task_id}"

        _logger.info("start push delete message to runtime")
        call_node_list = [item.get("node_id") for item in task_obj.node_list]
        message_dict = {
            "task_id": data.task_id,
            "node_id_list": call_node_list,
            "message_title": "task_delete",
            "message_time": int(time.time()),
            "message_content": {
                "task_id": data.task_id,
                "time": int(time.time()),
                "event": "task_delete"
            },
        }
        await push_message(message_dict)
        return True, ""
    except AssertionError as e:
        return False, str(e)


async def stop_running_task(db: AsyncSession, data: request.TaskIdModel) -> (bool, str):
    """
    停止正在运行的计算进程
    """
    try:
        async with db:
            select_sql = sqlalchemy.select(AutoMLTask).filter(AutoMLTask.task_id == data.task_id.strip())
            task_obj: AutoMLTask = (await db.execute(select_sql)).scalar_one_or_none()
            assert task_obj, f"get task failed by {data.task_id}"

        assert task_obj.status == MLTaskStatus.START, "未在运行的计算进程无需停止"
        assert os.environ.get("NODE_ID") == task_obj.initiator_node, "只有发起方才你那个发起停止任务"

        _logger.info("start push stop running message to runtime")
        call_node_list = [item.get("node_id") for item in task_obj.node_list]
        message_dict = {
            "task_id": data.task_id,
            "node_id_list": call_node_list,
            "message_title": "task_running_stop",
            "message_time": int(time.time()),
            "message_content": {
                "task_id": data.task_id,
                "time": int(time.time()),
                "event": "task_running_stop"
            },
        }
        await push_message(message_dict)
        return True, ""
    except AssertionError as e:
        return False, str(e)


async def reset_task(db: AsyncSession, data: request.TaskNodeModel) -> (bool, str):
    """
    重置运行失败的任务节点进程
    """
    try:
        async with db:
            select_sql = sqlalchemy.select(AutoMLTask).filter(AutoMLTask.task_id == data.task_id.strip())
            task_obj: AutoMLTask = (await db.execute(select_sql)).scalar_one_or_none()
            assert task_obj, f"get task failed by {data.task_id}"
            assert task_obj.status in (MLTaskStatus.START, MLTaskStatus.RUNNING_START_ERROR,
                                       MLTaskStatus.RUNNING_ERROR, MLTaskStatus.UPLOAD_ERROR,
                                       MLTaskStatus.FINISH_ERROR, MLTaskStatus.KILL_ERROR, MLTaskStatus.RESULT_UPLOAD
                                       ), f"启动或运行异常的任务才可以重启, {task_obj.status.name}"

        _logger.info("start push reset message to runtime")
        # call_node_list = [item.get("node_id") for item in task_obj.node_list]
        message_dict = {
            "task_id": data.task_id,
            "node_id_list": [data.node_id],
            "message_title": "task_reset",
            "message_time": int(time.time()),
            "message_content": {
                "reset_node_list": [data.node_id],
                "task_id": data.task_id,
                "time": int(time.time()),
                "event": "task_reset"
            },
        }
        await push_message(message_dict)
        return True, ""
    except AssertionError as e:
        return False, str(e)


async def update_task_progress(db: AsyncSession, data: request.TaskProgressModel) -> (bool, str):
    try:
        async with db:
            select_sql = sqlalchemy.update(AutoMLTask).where(AutoMLTask.task_id == data.task_id).values(
                progress_number=data.progress_number,
                update_at=datetime.datetime.now())
            await db.execute(select_sql)
            await db.commit()
            return True, ""
    except Exception as e:
        return False, e.__repr__()


async def push_message(data: dict, v_host="automl") -> (str):
    message_uuid = uuid.uuid4().hex + uuid.uuid4().hex
    try:
        data["message_uuid"] = message_uuid
        data["publish_node"] = os.environ.get("NODE_ID")
        credentials = pika.PlainCredentials(settings.MQ_USER_NAME, settings.MQ_USER_PASSWD)
        # 创建连接
        if v_host == "automl":
            virtual_host = settings.MQ_AUTO_HOST
        elif v_host == "federated":
            virtual_host = settings.MQ_FED_HOST
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.MQ_HOST, port=settings.MQ_PORT, virtual_host=virtual_host, credentials=credentials))
        # 建立信道
        channel = connection.channel()
        channel.exchange_declare(exchange=settings.MQ_EXCHANGE, exchange_type='fanout', durable=True)
        message = base64.b64encode(json.dumps(data, ensure_ascii=False).encode())
        channel.basic_publish(exchange=settings.MQ_EXCHANGE, routing_key='', body=message)
        _logger.info(f"push message {message}")
        connection.close()
        return message_uuid
    except pika_exceptions.UnroutableError as e:
        _logger.warning('Message was returned', e)
        return ""
    except pika_exceptions.NackError:
        _logger.warning('Message was NackError')
        return ""
    except pika_exceptions.StreamLostError:
        _logger.warning('连接不上代理服务器了！MQ突然的停止运行了！')
        return ""


async def pop_message(db: AsyncSession, data: request.MessagePopModel) -> (AutoMLReceiveMessage):
    async with db:
        select_sql = sqlalchemy.select(AutoMLReceiveMessage).where(
            AutoMLReceiveMessage.status == MessageConsumeStatus.INIT,
            AutoMLReceiveMessage.task_id == data.task_id).order_by(
            ~AutoMLReceiveMessage.id)
        message: AutoMLReceiveMessage = (await db.execute(select_sql)).scalars().first()
        if not message:
            return None
        message.consume_by = "system"
        message.consume_time = datetime.datetime.now()
        message.status = MessageConsumeStatus.CONSUME
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message


async def pop_fed_message(db: AsyncSession, data: request.MessagePopModel):
    async with db:
        select_sql = sqlalchemy.select(FedReceiveMessage).where(FedReceiveMessage.status == 0,
                                                                FedReceiveMessage.task_id == data.task_id).order_by(
            FedReceiveMessage.id)  # type: ignore
        message: FedReceiveMessage = (await db.execute(select_sql)).scalars().first()
        if not message:
            return None
        message.consume_by = "system"
        message.consume_time = datetime.datetime.now()
        message.status = 1
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message


async def push_file(data: request.FilePushModel, files: List[UploadFile] = None) -> (AutoMLReceiveMessage):
    cos_tools = CosTools(config=COS_SETTINGS)
    cos_tools.init_client()
    if data.durable:
        path = f"/task/{data.task_id}/store"
    else:
        path = f"/task/{data.task_id}/share"
    if files:
        file_obj = io.BytesIO(await files[0].read())
        flag, f_url = cos_tools.upload_file_obj(files[0].filename, file_obj, path=path)
    else:
        flag, f_url = cos_tools.upload_file_from_local(data.file_path, path=path)
    if not flag:
        return False, f"upload failed {data.file_path} !"
    else:
        return True, f_url


async def get_task_node_list(db: AsyncSession, data: request.TaskNodeListModel) -> (list, str):
    try:
        if data.task_type == 1:
            select_sql = sqlalchemy.select(FedCalculationTaskNode).filter(
                FedCalculationTaskNode.task_id == data.task_id)
            node_scalars = await db.execute(select_sql)
            return [line.to_dict() for line in node_scalars.scalars()], ""
        else:
            ret_list = []
            select_sql = sqlalchemy.select(AutoMLTask).filter(AutoMLTask.task_id == data.task_id.strip())
            task_obj: AutoMLTask = (await db.execute(select_sql)).scalar_one_or_none()
            assert task_obj, f"get task detail failed by {data.task_id}"
            for item in task_obj.node_list:
                ret_list.append({
                    "task_id": data.task_id,
                    "node_id": item.get("node_id"),
                    "role": 1 if task_obj.current_node_role == NodelRole.INITIATOR else 2,
                    "status": 1,
                    "dataset_status": 2,
                    "node_task_status": 0,
                    "verify_time": None,
                    "start_time": None,
                    "end_time": None
                })

            return ret_list, ""
    except AssertionError as e:
        return [], str(e)


async def get_fed_network_node_detail(db: AsyncSession, data: request.NodeIdModel):
    try:
        select_sql = sqlalchemy.select(FedCalculationNetworkNode).filter(
            FedCalculationNetworkNode.node_id == data.node_id)
        network_node: FedCalculationNetworkNode = (await db.execute(select_sql)).scalar_one_or_none()
        assert network_node, f"未找到该节点{data.node_id}的具体网路信息"
        return {
                   "node_id": data.node_id,
                   "node_ip": network_node.node_ip,
                   "node_name": network_node.node_name,
               }, ""
    except AssertionError as e:
        return {}, str(e)


async def get_task_log_list(db: AsyncSession, task_id: str) -> (list, str):
    try:
        async with db:
            select_sql = sqlalchemy.select(FedLog).filter(FedLog.task_id == task_id).order_by(desc(FedLog.create_at))
            task_scalars = await db.execute(select_sql)
            return [line.to_dict() for line in task_scalars.scalars()], ""
    except AssertionError as e:
        return [], str(e)
