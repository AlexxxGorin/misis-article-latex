#!/usr/bin/env python3
"""Render the reviewed Markdown manuscript into the MISiS LaTeX template."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "article.md"
TARGET = ROOT / "article.tex"

REF_KEYS = [
    "wendler2024llamas",
    "aghajanyan2020intrinsic",
    "hu2021lora",
    "hameed2024rosa",
    "pfeiffer2020mad",
    "csaki2023efficiently",
    "adelani2023sib",
    "africa2025meta",
    "podolskiy2025gamayun",
    "izmaylov2023rubert",
    "beresnev2023chatbots",
]


def escape_tex(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    return re.sub(r"[\\&%#_{}]", lambda m: replacements[m.group()], value)


def inline(value: str) -> str:
    protected: list[str] = []

    def hold(latex: str) -> str:
        protected.append(latex)
        return f"\u00a7{len(protected) - 1}\u00a7"

    value = re.sub(r"\$[^$]+\$", lambda m: hold(m.group()), value)
    value = re.sub(
        r"\[(\d+), табл\. (\d+)\]",
        lambda m: hold(rf"\cite[табл.~{m.group(2)}]{{{REF_KEYS[int(m.group(1)) - 1]}}}"),
        value,
    )
    value = re.sub(
        r"\[(\d+)–(\d+)\]",
        lambda m: hold(
            r"\cite{" + ",".join(REF_KEYS[n - 1] for n in range(int(m.group(1)), int(m.group(2)) + 1)) + "}"
        ),
        value,
    )
    value = re.sub(
        r"\[(\d+)\]",
        lambda m: hold(r"\cite{" + REF_KEYS[int(m.group(1)) - 1] + "}"),
        value,
    )
    value = re.sub(r"\*([^*]+)\*", lambda m: hold(r"\emph{" + escape_tex(m.group(1)) + "}"), value)
    value = escape_tex(value)
    return re.sub(r"\u00a7(\d+)\u00a7", lambda m: protected[int(m.group(1))], value)


def render(source: str) -> str:
    text, bibliography = source.split("## Литература\n", maxsplit=1)
    lines = text.splitlines()
    title = lines[0].removeprefix("# ").strip()
    author, affiliation, email = [part.strip() for part in lines[2].split("·")]
    supervisor = lines[4].strip()
    abstract = text.split("## Аннотация\n", maxsplit=1)[1].split("**Ключевые слова:**", maxsplit=1)[0].strip()
    keywords = text.split("**Ключевые слова:**", maxsplit=1)[1].split("\n", maxsplit=1)[0].strip().rstrip(".")
    body = text.split("## 1. Введение\n", maxsplit=1)[1]

    output = [
        "% Generated from article.md by scripts/render_article.py. Edit article.md.",
        r"\documentclass{misisarticle}",
        r"\IfFontExistsTF{Times New Roman}{}{",
        r"  \setmainfont{Liberation Serif}",
        r"  \let\cyrillicfont\relax",
        r"  \let\cyrillicfontsf\relax",
        r"  \let\cyrillicfonttt\relax",
        r"  \newfontfamily\cyrillicfont{Liberation Serif}",
        r"  \newfontfamily\cyrillicfontsf{Liberation Sans}",
        r"  \newfontfamily\cyrillicfonttt{Liberation Mono}",
        r"}",
        r"\grnti{28.23.37, 16.31.21}",
        r"\asjc{1702, 1706}",
        r"\oecd{1.02}",
        r"\title{" + escape_tex(title) + "}",
        r"\misisauthor{" + escape_tex(author) + "}{" + escape_tex(affiliation) + "}{Москва, Россия}{" + escape_tex(email) + "}",
        r"\abstract{" + inline(abstract) + "}",
        r"\keywords{" + inline(keywords.replace(";", ",")) + "}",
        r"\begin{document}",
        r"\maketitle",
        r"\noindent\emph{" + escape_tex(supervisor) + r"}\par",
        r"\section{Введение}",
    ]

    for paragraph in body.strip().split("\n\n"):
        paragraph = paragraph.strip()
        if paragraph.startswith("## "):
            heading = re.sub(r"^## \d+\. ", "", paragraph)
            output.extend(["", r"\section{" + escape_tex(heading) + "}"])
        elif paragraph.startswith("### "):
            heading = re.sub(r"^### \d+\.\d+\. ", "", paragraph)
            output.extend(["", r"\subsection{" + escape_tex(heading) + "}"])
        else:
            output.extend(["", inline(paragraph.replace("\n", " "))])

    refs = re.findall(r"^(\d+)\. (.+?) (https?://\S+)$", bibliography, re.MULTILINE)
    if len(refs) != len(REF_KEYS):
        raise ValueError(f"Expected {len(REF_KEYS)} references, found {len(refs)}")
    output.extend(["", r"\begin{thebibliography}{99}"])
    for expected, (index, entry, url) in enumerate(refs, start=1):
        if int(index) != expected:
            raise ValueError(f"Reference numbering jumps at {index}")
        output.append(r"\bibitem{" + REF_KEYS[expected - 1] + "} " + escape_tex(entry) + " " + r"\url{" + url + "}")
    output.extend([r"\end{thebibliography}", r"\end{document}", ""])
    return "\n".join(output)


if __name__ == "__main__":
    TARGET.write_text(render(SOURCE.read_text(encoding="utf-8")), encoding="utf-8")
    print(TARGET)
