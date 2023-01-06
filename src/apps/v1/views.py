# -*- coding: utf-8 -*-
import logging
import json
import time
import datetime
import os

from fastapi import Depends, Body, File, UploadFile
from typing import List
from starlette import status
from core.depends import get_database
from . import response
from . import request
from . import services
from fastapi.routing import APIRouter

from libs.framework_wraps.response import RetrieveResponse, ListResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import Optional

_logger = logging.getLogger("app")
router = APIRouter()


@router.post('/node/register',
             summary="注册节点",
             status_code=status.HTTP_200_OK,
             response_model=response.PostSuccessResponse
             )
async def register_node(db: Session = Depends(get_database),
                        data: request.NodeRegisterNodel = Body(...)):
    """
    注册节点
    """
    return_res, message = await services.register_node(db, data)
    _logger.info(f"service register node finish: {return_res}")
    if not return_res:
        return RetrieveResponse(content={}, code=-1,
                                message=f"node register failed! {message}")
    else:
        return RetrieveResponse(content=jsonable_encoder({"ok": ""}))

#
# @router.get('/automl/task/detail',
#             summary="获取任务详情",
#             status_code=status.HTTP_200_OK,
#             response_model=response.TaskDetailResponse
#             )
# async def auto_ml_task_detail(task_id: str, db: Session = Depends(get_database)):
#     """
#     获取任务详情:
#         task_id 任务ID
#     """
#
#     return_res, message = await services.get_task_detail(db, task_id)
#     _logger.info(f"service get task detail res={return_res} msg={message}")
#     if not return_res:
#         return RetrieveResponse(content={}, code=-1, message=message)
#     else:
#         if not return_res["calculation_time"]:
#             start_time = return_res["start_time"] if return_res["start_time"] else return_res["create_at"]
#             end_time = datetime.datetime.now() if not return_res["end_time"] else return_res["end_time"]
#             return_res["calculation_time"] = (end_time - start_time).seconds
#         return RetrieveResponse(content=jsonable_encoder(response.TaskDetailModel(**return_res).dict()))
#
#
# @router.get('/automl/task/list',
#             summary="获取任务列表",
#             status_code=status.HTTP_200_OK,
#             response_model=response.TaskDetailResponse
#             )
# async def auto_ml_task_list(db: Session = Depends(get_database)):
#     """
#     获取任务详情:
#         任务列表 任务ID
#     """
#     list_res = []
#     return_list, message = await services.get_task_list(db)
#     _logger.info(f"service get task detail res={len(return_list)} msg={message}")
#
#     for item in return_list:
#         if not item["calculation_time"]:
#             start_time = item["start_time"] if item["start_time"] else item["create_at"]
#             end_time = datetime.datetime.now() if not item["end_time"] else item["end_time"]
#             item["calculation_time"] = (end_time - start_time).seconds
#         list_res.append(response.TaskDetailModel(**item).dict())
#     return ListResponse(content=jsonable_encoder(list_res), current=1, size=len(list_res), total=len(list_res))
#
#
# @router.post('/automl/task/start',
#              summary="开始任务",
#              status_code=status.HTTP_200_OK,
#              response_model=response.TaskProgressResponse
#              )
# async def auto_ml_task_start(db: Session = Depends(get_database),
#                              data: request.TaskStartModel = Body(...)):
#     return_res, message = await services.start_task(db, data)
#     _logger.info(f"service create task finish: {return_res}")
#     if return_res:
#         return RetrieveResponse(content={"task_id": data.task_id})
#     else:
#         return RetrieveResponse(content={"task_id": data.task_id}, code=-1, message=message)
#
#
# @router.post('/automl/task/running/restart',
#              summary="重启任务",
#              status_code=status.HTTP_200_OK,
#              response_model=response.TaskProgressResponse
#              )
# async def auto_ml_task_restart(db: Session = Depends(get_database),
#                                data: request.TaskIdModel = Body(...)):
#     return_res, message = await services.restart_task(db, data)
#     _logger.info(f"service restart task finish: {return_res}")
#     if return_res:
#         return RetrieveResponse(content={"task_id": data.task_id})
#     else:
#         return RetrieveResponse(content={"task_id": data.task_id}, code=-1, message=message)
#
#
# @router.post('/automl/task/running/stop',
#              summary="停止计算任务",
#              status_code=status.HTTP_200_OK,
#              response_model=response.TaskProgressResponse
#              )
# async def auto_ml_task_restart(db: Session = Depends(get_database),
#                                data: request.TaskIdModel = Body(...)):
#     return_res, message = await services.stop_running_task(db, data)
#     _logger.info(f"service stop task finish: {return_res}")
#     if return_res:
#         return RetrieveResponse(content={"task_id": data.task_id})
#     else:
#         return RetrieveResponse(content={"task_id": data.task_id}, code=-1, message=message)
#
#
# @router.post('/task/delete',
#              summary="删除任务",
#              status_code=status.HTTP_200_OK, responses={400: {"model": {}}},
#              response_model=response.FilePushResponse
#              )
# async def auto_ml_task_delete(db: Session = Depends(get_database),
#                               data: request.TaskIdModel = Body(...)):
#     return_res, message = await services.delete_task(db, data)
#     _logger.info(f"service restart task finish: {return_res}")
#     if return_res:
#         return RetrieveResponse(content={"task_id": data.task_id})
#     else:
#         return RetrieveResponse(content={"task_id": data.task_id}, code=-1, message=message)
#
#
# @router.post('/task/running/reset',
#              summary="恢复节点任务",
#              status_code=status.HTTP_200_OK, responses={400: {"model": {}}},
#              response_model=response.FilePushResponse
#              )
# async def auto_ml_task_node_reset(db: Session = Depends(get_database),
#                                   data: request.TaskNodeModel = Body(...)):
#     return_res, message = await services.reset_task(db, data)
#     _logger.info(f"service reset task finish: {return_res}")
#     if return_res:
#         return RetrieveResponse(content={"task_id": data.task_id})
#     else:
#         return RetrieveResponse(content={"task_id": data.task_id}, code=-1, message=message)
#
#
# @router.post('/automl/task/progress',
#              summary="更新任务进度",
#              status_code=status.HTTP_200_OK,
#              response_model=response.TaskProgressResponse
#              )
# async def auto_ml_update_task_progress(db: Session = Depends(get_database),
#                                        data: request.TaskProgressModel = Body(...)):
#     return_res, message = await services.update_task_progress(db, data)
#     _logger.info(f"service update task progress  finish: {return_res}")
#     if return_res:
#         return RetrieveResponse(content={"task_id": data.task_id})
#     else:
#         return RetrieveResponse(content={"task_id": data.task_id}, code=-1, message=message)
#
#
# @router.post('/message/push',
#              summary="发送消息",
#              status_code=status.HTTP_200_OK, responses={400: {"model": {}}}
#              )
# async def push_message(db: Session = Depends(get_database),
#                        data: request.MessagePushModel = Body(...)):
#     message_uuid = await services.push_message(data.dict(), v_host=data.channel)
#     _logger.info(f"push_message {message_uuid}")
#     if message_uuid:
#         return RetrieveResponse(content={"message_uuid": message_uuid, "task_id": data.task_id})
#     else:
#         return RetrieveResponse(content={"message_uuid": message_uuid, "task_id": data.task_id}, code=-1,
#                                 message="push_message failed!")
#
#
# @router.post('/message/pop',
#              summary="获取消息",
#              status_code=status.HTTP_200_OK, responses={400: {"model": {}}}
#              )
# async def pop_message(db: Session = Depends(get_database),
#                       data: request.MessagePopModel = Body(...)):
#     if data.channel == "automl":
#         return_res = await services.pop_message(db, data)
#     else:
#         return_res = await services.pop_fed_message(db, data)
#
#     _logger.info(f"pop_message {return_res}")
#     if not return_res:
#         return RetrieveResponse(content={})
#     else:
#         res = return_res.to_dict()
#         if isinstance(res["message_content"], str):
#             res["message_content"] = json.loads(res["message_content"])
#         _logger.info(f"pop_message {res}")
#         return RetrieveResponse(content=jsonable_encoder(response.ResponseMessage(**res).dict()))
#
#
# @router.post('/file/upload',
#              summary="上传文件",
#              status_code=status.HTTP_200_OK, responses={400: {"model": {}}},
#              response_model=response.FilePushResponse
#              )
# async def push_file(db: Session = Depends(get_database), data: request.FilePushModel = Depends(),
#                     files: Optional[List[UploadFile]] = File(None)
#                     ):
#     ret_flag, f_url = await services.push_file(data, files=files)
#     _logger.info(f"push_file {data.file_path}")
#     if ret_flag:
#         ret_dict = data.dict()
#         ret_dict["f_url"] = f_url
#         return RetrieveResponse(content=jsonable_encoder(ret_dict))
#     else:
#         return RetrieveResponse(content={}, code=-1, message=f_url)
#
#
# @router.post('/task/nodelist',
#              summary="获取任务节点列表",
#              status_code=status.HTTP_200_OK, responses={400: {"model": {}}}
#              )
# async def get_task_node_list(db: Session = Depends(get_database),
#                              data: request.TaskNodeListModel = Body(...)):
#     ret_list, message = await services.get_task_node_list(db, data)
#     _logger.info(f"get task node list {data.task_id}")
#     if ret_list:
#         return ListResponse(content=jsonable_encoder(ret_list), current=1, size=len(ret_list), total=len(ret_list))
#     else:
#         return ListResponse(content=[], code=-1, message=message)
#
#
# @router.post('/fed/network/node/detail',
#              summary="网络节点详情",
#              status_code=status.HTTP_200_OK,
#              response_model=response.NodeDetailResponse
#              )
# async def fed_network_node_detail(db: Session = Depends(get_database),
#                                   data: request.NodeIdModel = Body(...)):
#     return_res, message = await services.get_fed_network_node_detail(db, data)
#     if return_res:
#         return RetrieveResponse(content=jsonable_encoder(response.NodeDetailModel(**return_res).dict()))
#     else:
#         return RetrieveResponse(content={}, code=-1, message=message)
#
#
# @router.get('/automl/log/list',
#             summary="获取任务列表",
#             status_code=status.HTTP_200_OK,
#             response_model=response.TaskLogListResponse
#             )
# async def task_log_list(task_id: str, db: Session = Depends(get_database)):
#     """
#     获取任务详情:
#         任务列表 任务ID
#     """
#     list_res = []
#     return_list, message = await services.get_task_log_list(db, task_id)
#     _logger.info(f"service get task log list res={len(return_list)} msg={message}")
#
#     for item in return_list:
#         list_res.append(response.TaskLogModel(**item).dict())
#     return ListResponse(content=jsonable_encoder(list_res), current=1, size=len(list_res), total=len(list_res))
