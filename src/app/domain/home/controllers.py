import structlog
from litestar import Controller, Request, get
from litestar.response import Template

__all__ = ("HomeController",)


logger = structlog.get_logger()


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

    # @get("/{filename:str}", tags=["frontend:"], include_in_schema=False)
    # async def get_resource(self, filename: str) -> Response:
    #     return Redirect(f"/static/{filename}")
