from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy.sql import sqltypes
import sqlalchemy
from sqlalchemy import Column
from enum import Enum
from sqlalchemy.orm import registry

mapper_registry = registry()


class IntEnum(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.Integer

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class NodeNetworkStatus(Enum):
    Disable = 0
    Online = 1
    Busy = 2
    Exception = -1
    Offline = -2


class NodeLicenseStatus(Enum):
    Disable = 0
    Valid = 1
    Overdue = -1


if TYPE_CHECKING:
    from .item import Item  # noqa: F401


@mapper_registry.mapped
@dataclass
class FederatedNode:
    __sa_dataclass_metadata_key__ = "sa"
    __tablename__ = 'federated_node'

    id: int = field(init=False, metadata={"sa": Column(sqltypes.BigInteger, primary_key=True, autoincrement=True)}, )
    create_at: Optional[datetime] = field(
        metadata={"sa": Column(sqltypes.DateTime(timezone=True), server_default=sqlalchemy.func.now(), )}, )
    update_at: Optional[datetime] = field(metadata={
        "sa": Column(sqltypes.DateTime(timezone=True), server_default=sqlalchemy.func.now(),
                     onupdate=datetime.now)}, )
    org_name: Optional[str] = field(
        metadata={"sa": Column(sqltypes.String(80), nullable=True, index=True, doc="组织名称")})
    org_id: Optional[str] = field(metadata={"sa": Column(sqltypes.String(80), nullable=True, index=True, doc="组织ID")})
    node_id: str = field(
        metadata={"sa": Column(sqltypes.String(80), nullable=False, index=True, unique=True, doc="节点ID")})
    node_ip: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False)})
    node_name: Optional[str] = field(
        metadata={"sa": Column(sqltypes.String(80), nullable=False, index=True, doc="节点名称")})

    content: str = field(metadata={"sa": Column(sqltypes.Text, nullable=True)})
    network_status: Optional[NodeNetworkStatus] = field(
        metadata={"sa": Column(IntEnum(NodeNetworkStatus), nullable=False, default=NodeNetworkStatus.Disable)})
    cpu: str = field(metadata={
        "sa": Column(sqltypes.Text, nullable=True, doc="处理器【宿主机监控显示的cpu为超线程数量,虚拟机为核数】")})
    gpu: str = field(metadata={"sa": Column(sqltypes.Text, nullable=True, doc="gpu")})
    memory: str = field(metadata={"sa": Column(sqltypes.Text, nullable=True, doc="内存")})
    disk: str = field(metadata={"sa": Column(sqltypes.Text, nullable=True, doc="硬盘")})
    registry_date: datetime.date = field(metadata={"sa": Column(sqltypes.Date, nullable=True, doc="注册日期")})
    machine_code: str = field(metadata={"sa": Column(sqltypes.String(100), nullable=True, doc="机器码")})
    license_code: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False, doc="license串")})
    license_status: Optional[NodeLicenseStatus] = field(
        metadata={"sa": Column(IntEnum(NodeLicenseStatus), nullable=False, default=NodeLicenseStatus.Disable)})

    def to_dict(self):
        return {c.name: getattr(self, c.name, None).value if isinstance(getattr(self, c.name, None), Enum) else getattr(
            self, c.name, None) for c in self.__table__.columns}


@mapper_registry.mapped
@dataclass
class NodeDevOverview:
    __sa_dataclass_metadata_key__ = "sa"
    __tablename__ = 'node_dev_overview'

    id: int = field(init=False, metadata={"sa": Column(sqltypes.BigInteger, primary_key=True, autoincrement=True)}, )
    create_at: Optional[datetime] = field(
        metadata={"sa": Column(sqltypes.DateTime(timezone=True), server_default=sqlalchemy.func.now())}, )
    update_at: Optional[datetime] = field(metadata={
        "sa": Column(sqltypes.DateTime(timezone=True), server_default=sqlalchemy.func.now())}, )
    node_id: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False, index=True, doc="节点ID")})
    dev_type: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False, doc="设备类型")})
    dev_name: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False, doc="设备名称")})
    content: dict = field(metadata={"sa": Column(sqltypes.JSON, nullable=False, doc="设备概况")})

    def to_dict(self):
        return {c.name: getattr(self, c.name, None).value if isinstance(getattr(self, c.name, None), Enum) else getattr(
            self, c.name, None) for c in self.__table__.columns}


@mapper_registry.mapped
@dataclass
class NodeLicense:
    __sa_dataclass_metadata_key__ = "sa"
    __tablename__ = 'node_license'

    id: int = field(init=False, metadata={"sa": Column(sqltypes.BigInteger, primary_key=True, autoincrement=True)}, )
    create_at: Optional[datetime] = field(
        metadata={"sa": Column(sqltypes.DateTime(timezone=True), server_default=sqlalchemy.func.now())}, )
    update_at: Optional[datetime] = field(metadata={
        "sa": Column(sqltypes.DateTime(timezone=True), server_default=sqlalchemy.func.now())}, )
    node_id: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False, index=True, doc="节点ID")})
    license_code: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False, doc="license串")})
    status: Optional[NodeLicenseStatus] = field(
        metadata={"sa": Column(IntEnum(NodeLicenseStatus), nullable=False, default=NodeLicenseStatus.Disable)})

    def to_dict(self):
        return {c.name: getattr(self, c.name, None).value if isinstance(getattr(self, c.name, None), Enum) else getattr(
            self, c.name, None) for c in self.__table__.columns}


@mapper_registry.mapped
@dataclass
class NodeInitRecord:
    __sa_dataclass_metadata_key__ = "sa"
    __tablename__ = 'node_init_record'

    id: int = field(init=False, metadata={"sa": Column(sqltypes.BigInteger, primary_key=True, autoincrement=True)}, )
    create_at: Optional[datetime] = field(
        metadata={"sa": Column(sqltypes.DateTime(timezone=True), server_default=sqlalchemy.func.now())}, )
    update_at: Optional[datetime] = field(metadata={
        "sa": Column(sqltypes.DateTime(timezone=True), server_default=sqlalchemy.func.now())}, )
    node_id: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False, index=True, doc="节点ID")})
    node_init_type: str = field(metadata={"sa": Column(sqltypes.String(80), nullable=False, index=True,
                                                       doc="初始化流程类型 chain_connector, playground")})
    init_result: bool = field(metadata={"sa": Column(sqltypes.BOOLEAN, nullable=False, index=True, doc="初始化结果")})
    init_content: str = field(metadata={"sa": Column(sqltypes.JSON, nullable=False, doc="各种杂乱的配置信息")})
    message: str = field(metadata={"sa": Column(sqltypes.Text, nullable=False, doc="错误信息")})

    def to_dict(self):
        return {c.name: getattr(self, c.name, None).value if isinstance(getattr(self, c.name, None), Enum) else getattr(
            self, c.name, None) for c in self.__table__.columns}
