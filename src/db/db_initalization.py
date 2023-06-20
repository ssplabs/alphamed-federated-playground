import sqlalchemy
import datetime

from sqlalchemy import column

from db.models import NodeInitRecord
from core.database import SessionLocal


def check_init_step(node_id, init_type="chain_connector"):
    with SessionLocal() as db_session:
        query = sqlalchemy.select(NodeInitRecord).where(column('node_init_type') == init_type).where(
            column("node_id") == node_id)
        ret: NodeInitRecord = db_session.execute(query).scalar_one_or_none()
    if ret:
        return ret
    else:
        return create_init_step(node_id, init_type=init_type)


def create_init_step(node_id, init_type="chain_connector"):
    with SessionLocal() as db_session:
        value_dict = {
            "create_at": datetime.datetime.now(),
            "update_at": datetime.datetime.now(),
            "node_id": node_id,
            "node_init_type": init_type,
            "init_result": False,
            "init_content": {},
            "message":""
        }
        ret = NodeInitRecord(**value_dict)
        db_session.add(ret)
        db_session.commit()
        db_session.refresh(ret)
    return ret


def update_step(node_id, init_type, step_result: bool, message: str):
    with SessionLocal() as db_session:
        query = sqlalchemy.select(NodeInitRecord).where(column('node_init_type') == init_type).where(
            column("node_id") == node_id)
        # node_step: NodeInitRecord = db_session.execute(query).scalar_one_or_none()
