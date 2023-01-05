from datetime import datetime
from pydantic import BaseConfig, BaseModel, Field
from typing import Optional, List


class TaskDetailModel(BaseModel):
    task_id: str = None
    task_name: str = None
    status: int = 0
    description: str
    dataset_id: str
    dataset_version: str
    model_name: str
    model_id: str
    report: Optional[str]
    result_model: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    node_list: list
    calculation_type: int = Field(description="计算类型 1 横向联邦 2 异构联邦 3 单机训练", default=1)
    calculation_time: Optional[int]
    forecast_calculation_time: Optional[int]
    initiator_node: str
    current_node_role: int = Field(description="当前节点角色 1 发起者 2 参与者")
    created_by: str
    progress_number: int = Field(description="进度值 0-100")
    message: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "task_id": "任务ID",
                "task_name": "任务名称",
                "message": "数据集校验失败",
                "status": "INIT = 0 初始化 PENDING = 1  # 进入计算侧进程 ENV_READY = 2  # 数据环境准备完毕 DATA_VERIFY = 3  # 数据校验完成 JOIN_NETWORK = 4  # 加入计算网络 START = 5  # 开始运行 RESULT_UPLOAD = 6  # 结果上传完毕 FINISHED = 7  # 运行结束 PENDING_ERROR = -1  # 计算环境加载失败 ENV_ERROR = -2  # 数据环境加载失败 DATA_VERIFY_ERROR = -3  # 数据校验失败 JOIN_NETWORK_ERROR = -4  # 加入计算网络失败 RUNNING_START_ERROR = -5  # 计算程序启动异常 RUNNING_ERROR = -6  # 计算程序运行异常 UPLOAD_ERROR = -7  # 运算报告结果检测异常 FINISH_ERROR = -8  # 计算程序结束异常 KILL_ERROR = -9  # 强制结束计算程序 UNKNOWN_ERROR = -10  # 未知状态",
                "description": "任务描述",
                "dataset_id": "数据集ID",
                "dataset_version": "数据集版本",
                "model_name": "预训练模型名称",
                "model_id": "预训练模型ID",
                "report": "训练报告地址",
                "result_model": "结果模型地址",
                "start_time": "开始训练时间",
                "end_time": "结束训练时间",
                "calculation_type": 0,
                "calculation_time": 1000,
                "forecast_calculation_time": 3000,
                "initiator_node": "QmWuc1GSaqCkUajoPG5QHfeh72YqU4N7VH7Nx2eP6FyJ9M",
                "current_node_role": 1,
                "progress_number": 20,
                "created_by": "system",
                "node_list": [
                    "QmegaqF4RjBjN3i4NdJy24svtFkJAUXc3YUFqRKqNjaAw4",
                    "QmegaqF4RjBjN3i4NdJy24svtFkJAUXc3YUFqRKqNjaAw4"
                ],
            }

        }


class TaskDetailResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: TaskDetailModel


class ResponseMessage(BaseModel):
    id: int = None
    task_id: str = None
    node_id_list: list = None
    consume_by: str
    consume_time: datetime
    message_uuid: str
    message_title: str
    message_content: dict
    message_time: int
    status: int = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "id": "消息ID",
                "task_id": "任务ID",
                "node_id_list": ["*"],
                "consume_time": "",
                "consume_by": "node01",
                "message_time": 1658829147,
                "message_uuid": "69dfe7f9-3e2f-411b-bc01-24f4cf381641",
                "message_title": "ApplySendingDataEvent",
                "message_content": {},
                "status": 1,
            }

        }




class TaskIdModel(BaseModel):
    task_id: str = None


class TaskProgressResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: TaskIdModel


class FilePushResponse(BaseModel):
    task_id: str = Field(description="任务ID")
    file_path: str = Field(description="上传文件")
    durable: bool = Field(description="持久化存储, 参数非持久，报告、模型持久存储")
    f_url: str = Field(description="文件共享URL")


class NodeDetailModel(BaseModel):
    node_id: Optional[str] = Field(description="节点ID")
    node_ip: Optional[str] = Field(description="节点IP")
    node_name: Optional[str] = Field(description="节点名称")


class NodeDetailResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: NodeDetailModel


class TaskLogModel(BaseModel):
    task_id: str
    node_id: Optional[str]
    content: Optional[str]
    create_at: Optional[datetime]


class TaskLogDetailModel(BaseModel):
    current: int
    page: int
    records: Optional[List[TaskLogModel]]
    size: int
    total: int


class TaskLogListResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: TaskLogDetailModel
