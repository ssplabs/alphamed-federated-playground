import re
from pydantic import BaseModel, validator, ValidationError, constr
from pydantic.fields import ModelField
from typing import Optional
from pydantic import Field



class TaskCreateModel(BaseModel):
    task_id: str = Field(description="任务ID", max_length=80, min_length=20)
    # node_list: list = Field(description="参与节点的列表")
    task_name: str = Field(description="名称")
    description: str = Field(description="任务描述")
    publish_node: str = Field(description="发布节点")
    dataset_id: str = Field(description="数据集ID")
    dataset_version: str = Field(description="数据集版本")
    model_name: str = Field(description="预训练模型名称")
    model_id: str = Field(description="预训练模型ID")
    current_node: str = Field(description="当前节点")
    calculation_type: int = Field(description="计算类型 1 横向联邦 2 异构联邦 3 单机训练", default=1)

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
            # "node_list": [
            #     "QmWuc1GSaqCkUajoPG5QHfeh72YqU4N7VH7Nx2eP6FyJ9M",
            #     "QmegaqF4RjBjN3i4NdJy24svtFkJAUXc3YUFqRKqNjaAw4",
            #     "QmP4DksaGVrFgkNp3d4NxZnnb4RtQucpMqLESJTAEAtuxC",
            #     "QmRj3kV7uQeCndrJvYYFHwfDoQmFdxNkCqpiL7m7VanKfw"
            # ],
            "task_description": "This is a test automl project",
            "model_name": "skin_lesion_diagnosis_fed_avg",
            "model_id": "51f8f62d-9264-4724-ba73-fc7786743209",
            "dataset_id": "3f7ebc052a0142249dcae8d47141e488",
            "dataset_version": "3f7ebc052a0142249dcae8d47141e488"
        }


class TaskStartModel(BaseModel):
    task_id: str = Field(description="任务ID", max_length=80, min_length=20)
    node_list: list = Field(description="参与节点的列表")

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
            "node_list": [
                "QmWuc1GSaqCkUajoPG5QHfeh72YqU4N7VH7Nx2eP6FyJ9M",
                "QmegaqF4RjBjN3i4NdJy24svtFkJAUXc3YUFqRKqNjaAw4",
                "QmP4DksaGVrFgkNp3d4NxZnnb4RtQucpMqLESJTAEAtuxC",
                "QmRj3kV7uQeCndrJvYYFHwfDoQmFdxNkCqpiL7m7VanKfw"
            ]
        }


class TaskProgressModel(BaseModel):
    task_id: str = Field(description="任务ID", max_length=80, min_length=20)
    progress_number: int = Field(description="进度", ge=0, le=100)

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
            "progress_number": 10
        }


class TaskIdModel(BaseModel):
    task_id: str = Field(description="任务ID")

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
        }


class MessagePopModel(BaseModel):
    task_id: str = Field(description="任务ID")
    channel: Optional[str] = Field(description="任务ID", default="automl")

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
        }


class TaskNodeListModel(BaseModel):
    task_id: str = Field(description="任务ID")
    task_type: int

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
            "task_type": "1 自主训练,2 自动化建模",
        }


class MessagePushModel(BaseModel):
    task_id: str = Field(description="任务ID")
    node_id_list: list = Field(description="参与节点的列表")
    message_title: str = Field(description="消息主题")
    message_content: dict = Field(description="消息内容详情")
    message_time: int = Field(description="消息时间")
    channel: Optional[str] = Field(description="消息时间", default="automl")

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
            "message_time": 1666958489,
            "node_id_list": [
                "QmWuc1GSaqCkUajoPG5QHfeh72YqU4N7VH7Nx2eP6FyJ9M",
                "QmegaqF4RjBjN3i4NdJy24svtFkJAUXc3YUFqRKqNjaAw4",
                "QmP4DksaGVrFgkNp3d4NxZnnb4RtQucpMqLESJTAEAtuxC",
                "QmRj3kV7uQeCndrJvYYFHwfDoQmFdxNkCqpiL7m7VanKfw",
                "QmYX5KatFyFve3xVjadX2h7fEt1SzpdA8wnQsQ4v9muCyR"
            ],
            "message_title": "TaskSync",
            "channel": "automl",
            "message_content": {
                "task_id": "3f7ebc052a0142249dcae8d47141e488",
                "event": "task_pending"
            },
        }


class FilePushModel(BaseModel):
    task_id: str = Field(description="任务ID")
    file_path: Optional[str] = Field(description="文件在存储中的相对路径")
    durable: bool = Field(description="持久化存储, 参数非持久，报告、模型持久存储")

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
            "file_path": "/tmp/ffff.xml",
            "upload_type": True
        }


class NodeIdModel(BaseModel):
    node_id: str = Field(description="节点ID")

    class config:
        schema_extra = {
            "node_id": "3f7ebc052a0142249dcae8d47141e488"
        }


class TaskNodeModel(BaseModel):
    task_id: str = Field(description="任务ID")
    node_id: str = Field(description="节点ID")

    class config:
        schema_extra = {
            "task_id": "3f7ebc052a0142249dcae8d47141e488",
            "node_id": "3f7ebc052a0142249dcae8d47141e488"
        }

