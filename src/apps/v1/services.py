import base64
import io
import time
import datetime
import logging
import uuid

import json
import os
from typing import List
import sqlalchemy
import datetime
from core import settings
from fastapi import UploadFile
from . import request
import hashlib
from sqlalchemy import column, desc

from db.models import FederatedNode, NodeLicense, NodeLicenseStatus, NodeNetworkStatus
from sqlalchemy.orm import Session
from libs.other_utils import ExecShellUnix

_logger = logging.getLogger("app")


def check_license(db: Session, license_code):
    res = ExecShellUnix("dmidecode -s  system-serial-number")
    assert res, "system error os should install dmidecode package"
    machine_code = res[0].strip()
    node_id = hashlib.md5(machine_code.encode()).hexdigest().upper()
    local_license_code = hashlib.sha256(node_id.encode()).hexdigest().upper()
    assert local_license_code == license_code
    query = sqlalchemy.select(NodeLicense).where(column('license_code') == license_code)
    node_license: NodeLicense = db.execute(query).scalar_one_or_none()
    if node_license:
        node_license.node_id = node_id
        node_license.status = NodeLicenseStatus.Valid
        node_license.update_at = datetime.datetime.now()
        db.commit()
    else:
        node_license = NodeLicense({
            "create_at": datetime.datetime.now(),
            "update_at": datetime.datetime.now(),
            "node_id": node_id,
            "license_code": license_code,
            "status": NodeLicenseStatus.Valid,
        })
        db.add(node_license)
        db.commit()
    db.refresh(node_license)
    return node_license


async def register_node(db: Session, data: request.NodeRegisterNodel):
    try:
        message = ""
        up_dict = {
            "status": NodeNetworkStatus.Online,
            "update_at": datetime.datetime.now()
        }
        node_license = check_license(license_code=data.license_code)

        up_sql = sqlalchemy.update(FederatedNode).where(
            FederatedNode.node_id == node_license.node_id).values(**up_dict)
        db.execute(up_sql)
        db.commit()
    except AssertionError as e:
        message = e.__repr__()
    except Exception as e:
        _logger.exception(e)
        message = "秘钥校验服务异常!"
    if message:
        return False, message
