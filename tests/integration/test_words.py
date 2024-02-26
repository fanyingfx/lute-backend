import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    ("word_id", "expected_status_code"),
    (
        ("3", 404),
        ("1", 200),
    ),
)
async def test_query_by_word_id(client: AsyncClient, word_id: int, expected_status_code: int) -> None:
    response = await client.get(f"/word/word_id/{word_id}")
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(("word_string", "expected_status_code"), (("hello", 200), ("nice", 404)))
async def test_search_word(client: AsyncClient, word_string: str, expected_status_code: int) -> None:
    response = await client.get(f"/word/word_string/{word_string}")
    assert response.status_code == expected_status_code
