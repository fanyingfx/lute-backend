from litestar import Request
from litestar import get
from litestar.response import Template

__all_=["home"]
@get(path="/", operation_id="home", tags=["frontend:home"], status_code=200, include_in_schema=False)
async def home(request: Request) -> Template:
    """Index page.

    Args:
        request: Request object

    Returns:
        Tuple: Response and status code
    """
    request.logger.info("Index page requested.")
    context = {
        "request": request,
        "repo_url": "https://github.com/JacobCoffee/litestar-template",
        "railway_ref_url": "https://railway.app/template/zx1KGh?referralCode=BMcs0x",
    }
    return Template("index.html", context=context)

