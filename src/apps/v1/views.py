# -*- coding: utf-8 -*-
import logging

from fastapi import Depends, Body
from starlette import status
from core.depends import get_database
from . import response
from . import request
from . import services
from fastapi.routing import APIRouter

from libs.framework_wraps.response import RetrieveResponse, ListResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

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
