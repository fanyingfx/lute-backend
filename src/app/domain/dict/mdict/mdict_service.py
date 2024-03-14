from pathlib import Path

from query.mdict_utils import MDXDict

MDX_FILE = "D:/Code/mdict-query/mdx/olad10/Oxford Advanced Learner's Dictionary 10th.mdx"
MDXPATH = Path(MDX_FILE)

mdx_dict = MDXDict(MDXPATH)


def hello_mdict() -> bytes:
    return mdx_dict.lookup("hello")  # type: ignore


# if __name__=='__main__':
#
#     res=mdx_dict.lookup('hello')
#     s=res.decode('utf8')
