# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter


from .views import router as router_token

router = APIRouter()
router.include_router(router_token)
