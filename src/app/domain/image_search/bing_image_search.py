import asyncio
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup

__all__ = ["fetch_all_images"]


async def _fetch_image_urls(search_query: str, page_num: int) -> list[str]:
    search_url = f"https://www.bing.com/images/search?q={quote_plus(search_query)}&first={page_num}&count=40"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.11 (KHTML, like Gecko) "
        "Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            image_urls = []

            for img in soup.find_all("img"):
                src = img.get("src")
                if src and src.startswith("http"):
                    image_urls.append(src)

            return image_urls

        except httpx.HTTPStatusError:
            return []


async def fetch_all_images(search_query: str, num_pages: int = 2) -> list[str]:
    tasks = [_fetch_image_urls(search_query, page) for page in range(num_pages)]
    results = await asyncio.gather(*tasks)
    return list({url for urls in results for url in urls})


async def main(search_query):  # type: ignore
    await fetch_all_images(search_query)


if __name__ == "__main__":
    asyncio.run(main("cat"))  # type: ignore
