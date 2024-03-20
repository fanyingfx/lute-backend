from pathlib import Path


def get_book(path: Path) -> str:
    with open(path, encoding="utf-8") as f:  # noqa
        return f.read()


def get_en_book() -> str:
    return get_book(Path(__file__).parent / "demo_books" / "en.md")


def get_jp_book() -> str:
    return get_book(Path(__file__).parent / "demo_books" / "jp.md")


# if __name__ == '__main__':
#
#     print(en_book_text)
