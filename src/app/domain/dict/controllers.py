from litestar import Controller, MediaType, get
from litestar.response import Response
from mdict_query.mdict_utils import content_type_map

from .mdict.mdict_service import en_mdx_dict, en_query, jp_mdx_dict, jp_query


class DictController(Controller):
    path = "/dict"
    tags = ["dict"]

    @get(path="/{filename:str}", cache=True)
    async def get_resource(self, filename: str) -> Response:
        ext = filename.split(".")[-1]
        res = en_mdx_dict.lookup(filename) or jp_mdx_dict.lookup(filename)

        response_media_type = content_type_map[ext]

        return Response(res, media_type=response_media_type)

    @get(path="/en", media_type=MediaType.HTML)
    async def query_en_word(self, word: str) -> bytes:
        return en_query(word)

    @get(path="/jp", media_type=MediaType.HTML)
    async def query_jp_word(self, word: str) -> bytes:
        return jp_query(word)
