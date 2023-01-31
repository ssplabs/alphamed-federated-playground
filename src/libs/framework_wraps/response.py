import json
import typing
import math

from starlette.background import BackgroundTask

from starlette.responses import JSONResponse


class RetrieveResponse(JSONResponse):

    def __init__(self,
                 content: typing.Any = None,
                 code: int = 0,
                 message: str = "",
                 headers: dict = None,
                 media_type: str = None,
                 background: BackgroundTask = None, ):
        self.code = code
        self.message = message
        super(RetrieveResponse, self).__init__(content, 200, headers, media_type, background)

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            {"code": self.code, "message": self.message, "data": content},
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


class ListResponse(JSONResponse):

    def __init__(self,
                 content: typing.Any = None,
                 code: int = 0,
                 message: str = "",
                 headers: dict = None,
                 media_type: str = None,
                 background: BackgroundTask = None, current=1, size=20, total=None):
        self.code = code
        self.message = message
        self.current = current
        self.page = 1
        self.size = size
        self.total = total
        super(ListResponse, self).__init__(content, 200, headers, media_type, background)

    def render(self, content: typing.List) -> bytes:
        self.page = math.ceil(self.total / self.size) if self.total else 1
        return json.dumps(
            {"code": self.code, "message": self.message, "data": {
                "current": self.current,
                "page": self.page,
                "records": content,
                "size": self.size,
                "total": self.total if self.total else len(content)
            }
             },
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
