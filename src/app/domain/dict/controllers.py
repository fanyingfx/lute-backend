from litestar import Controller, MediaType, get
from litestar.response import Response
from query.mdict_utils import content_type_map

from .mdict.mdict_service import hello_mdict, mdx_dict


class DictController(Controller):
    path = "/dict"
    tags = ["dict"]

    @get(path="/{filename:str}")
    async def get_resource(self, filename: str) -> Response:
        ext = filename.split(".")[-1]
        # if filename in mdx_dict.local_map:
        #     res = mdx_dict.local_map[filename]
        # else:
        #     res = mdx_dict.lookup(f"/{filename}")
        res = mdx_dict.local_map[filename] if filename in mdx_dict.local_map else mdx_dict.lookup(f"/{filename}")
        return Response(res, media_type=content_type_map[ext])

    @get(path="/en", media_type=MediaType.HTML)
    async def test_hello(self) -> bytes:
        return hello_mdict()
