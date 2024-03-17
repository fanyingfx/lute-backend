from litestar import Controller, get
from litestar.response import Redirect, Template
from litestar.status_codes import HTTP_200_OK

# from app.config import constants


class WebController(Controller):
    """Web Controller."""

    include_in_schema = False
    opt = {"exclude_from_auth": True}

    @get("/", operation_id="WebIndex", name="frontend:index", status_code=HTTP_200_OK)
    async def index(self) -> Template:
        """Serve site root."""
        return Template(template_name="index.html")

    @get("/{filename:str}")
    async def get_static_resource(self, filename: str) -> Redirect:
        """
        redirect for favicon.ico
        """
        if "ico" not in filename:
            return Redirect(f"/dict/{filename}")
        return Redirect(f"/static/{filename}")
