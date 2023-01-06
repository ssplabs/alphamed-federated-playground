from datetime import datetime
from pydantic import BaseConfig, BaseModel, Field
from typing import Optional, List


class SuccessMessage(BaseModel):
    ok: str = ""

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "ok": ""
            }

        }


class PostSuccessResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: SuccessMessage


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
