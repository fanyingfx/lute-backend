from pathlib import Path

from mdict_query.mdict_utils import MDXDict

EN_MDX_FILE = "D:/Code/mdict-query/mdx/olad10/Oxford Advanced Learner's Dictionary 10th.mdx"
EN_MDXPATH = Path(EN_MDX_FILE)
en_mdx_dict = MDXDict(EN_MDXPATH)

JP_MDX_FILE = "C:/Users/fanzh/PycharmProjects/lute-backend/data/dicts/ja/Shogakukanjcv3/Shogakukanjcv3.mdx"
JP_MDXPATH = Path(JP_MDX_FILE)
jp_mdx_dict = MDXDict(JP_MDXPATH)


def en_query(word: str) -> bytes:
    return en_mdx_dict.lookup(word)  # type: ignore[no-any-return]


def jp_query(word: str) -> bytes:
    return jp_mdx_dict.lookup(word)  # type: ignore[no-any-return]


# if __name__=='__main__':
#
#     res=mdx_dict.lookup('hello')
#     s=res.decode('utf8')
