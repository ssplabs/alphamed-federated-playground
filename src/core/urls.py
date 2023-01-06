# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter
from apps.v1.urls import router as router_v1_app


router = APIRouter()
router.include_router(router_v1_app, prefix='/fed-node-service/api/v1', tags=['federated-node-service-V1'])
