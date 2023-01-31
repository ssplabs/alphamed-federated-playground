import re
from pydantic import BaseModel, validator, ValidationError, constr
from pydantic.fields import ModelField
from typing import Optional
from pydantic import Field


class NodeRegisterNodel(BaseModel):
    license_code: str = Field(description="license_code", max_length=80, min_length=20)

    class Config:
        schema_extra = {
            "license_code": "89AC2AD866CED3157F8B8B22FB5DF8332A7328708425719F3A1A108D007C28C8",
        }
