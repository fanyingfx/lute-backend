from litestar import Controller, Request, Response, get
from litestar.response import Redirect, Template

from app.lib import log

__all__ = ("HomeController",)

__all_ = ["HomeController"]

logger = log.get_logger()


class HomeController(Controller):
    @get(path="/", operation_id="home", tags=["frontend:home"], status_code=200, include_in_schema=False)
    async def home(self, request: Request) -> Template:
        """Index page.

        Args:
            request: Request object

        Returns:
            Tuple: Response and status code
        """
        logger.info("Index page requested.")
        context = {
            "request": request,
            "repo_url": "https://github.com/JacobCoffee/litestar-template",
            "railway_ref_url": "https://railway.app/template/zx1KGh?referralCode=BMcs0x",
        }
        return Template("index.html", context=context)

    @get("/favicon.ico", tags=["frontend:"], include_in_schema=False)
    async def get_resource(self, path: str) -> Response:
        return Redirect("/static/favicon.ico")
