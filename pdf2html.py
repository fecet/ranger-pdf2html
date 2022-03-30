#!/usr/bin/env python

# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3

# %%

from bs4 import BeautifulSoup
import argparse
from pathlib import Path
import subprocess

# %%


parser = argparse.ArgumentParser()
# parser.add_argument(
#     "--pdf-path", "-p", dest="pdf_path", help="pdf document path", required=True
# )
parser.add_argument("pdf_path", help="The PDF document file path to be converted")
parser.add_argument(
    "html_path", nargs="?", default="", help="The HTML document file path to be stored"
)
parser.add_argument(
    "--open_files", "-o", help="Open html and PDF files", action="store_true"
)
args = parser.parse_args()


# %%


def pdf2html(pdf_path, html_path="", open_files=False):

    pdf_path = Path(pdf_path)  # pdf_path = Path("test.pdf")
    html_path = (
        Path(html_path) if html_path else pdf_path.parent / f"{pdf_path.stem}.html"
    )
    if not html_path.exists():
        subprocess.run(["pdf2htmlEX", pdf_path, html_path])
        # Post process for the HTML file
        # Delete TOC
        with open(html_path, "r+") as f:
            soup = BeautifulSoup(f, "html.parser")
            elements = soup.find_all("div", id="sidebar")
            for element in elements:
                element.decompose()

            f.write(str(soup))
    if open_files:

        subprocess.Popen(["xdg-open", pdf_path], start_new_session=True)
        subprocess.Popen(["xdg-open", html_path], start_new_session=True)


# %%

if __name__ == "__main__":
    pdf2html(args.pdf_path, args.html_path, args.open_files)
