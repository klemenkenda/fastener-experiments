"""Fetch one arXiv paper for a FASTENER paper repository's related work.

Reads the arXiv API (title, authors, first-version date, latest version,
category, abstract) and the abstract page's licence link, downloads the PDF
into a fresh temporary directory, checks it is a PDF and hashes it. The PDF
is copied into <paper repo>/related-work/ only when the licence allows
redistribution (CC BY, CC BY-SA, CC0, and their versions); otherwise the
paper is linked, not kept. Prints a JSON record for BIBLIOGRAPHY.md.

    python fetch_arxiv.py 2510.20351 "papers/P5 - What LLMs Know About Benchmark Datasets"
    python fetch_arxiv.py 2510.20351 <paper repo> --dry-run     # nothing copied
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UA = {"User-Agent": "fastener-related-work/1.0 (klemen.kenda@ijs.si)"}
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
# Licences that allow anyone to redistribute the PDF (with attribution).
REDISTRIBUTABLE = ("creativecommons.org/licenses/by/", "creativecommons.org/licenses/by-sa/",
                   "creativecommons.org/publicdomain/zero/")


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def metadata(arxiv_id: str) -> dict:
    root = ET.fromstring(get(f"https://export.arxiv.org/api/query?id_list={arxiv_id}"))
    e = root.find(f"{ATOM}entry")
    if e is None or e.find(f"{ATOM}title") is None:
        sys.exit(f"arXiv has no entry {arxiv_id}")
    abs_id = e.find(f"{ATOM}id").text.rsplit("/", 1)[-1]          # e.g. 2510.20351v4
    clean = lambda t: re.sub(r"\s+", " ", t or "").strip()
    doi = e.find(f"{ARXIV}doi")
    jref = e.find(f"{ARXIV}journal_ref")
    return {
        "arxiv_id": arxiv_id, "version_id": abs_id,
        "version": int(re.search(r"v(\d+)$", abs_id).group(1)),
        "title": clean(e.find(f"{ATOM}title").text),
        "authors": [clean(a.find(f"{ATOM}name").text) for a in e.findall(f"{ATOM}author")],
        "first_version": e.find(f"{ATOM}published").text[:10],
        "this_version": e.find(f"{ATOM}updated").text[:10],
        "category": e.find(f"{ARXIV}primary_category").get("term"),
        "doi": doi.text if doi is not None else None,
        "journal_ref": clean(jref.text) if jref is not None else None,
        "abstract": clean(e.find(f"{ATOM}summary").text),
    }


def licence(arxiv_id: str) -> str | None:
    page = get(f"https://arxiv.org/abs/{arxiv_id}").decode("utf-8", "replace")
    m = re.search(r'href="(https?://(?:creativecommons\.org|arxiv\.org/licenses)[^"]+)"', page)
    return m.group(1) if m else None


def slug(title: str, words: int = 5) -> str:
    stop = {"a", "an", "the", "of", "for", "in", "on", "and", "to", "with", "when", "via"}
    w = [x for x in re.findall(r"[a-z0-9]+", title.lower()) if x not in stop]
    return "-".join(w[:words])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("arxiv_id", help="e.g. 2510.20351 (latest version) or 2510.20351v2")
    ap.add_argument("paper_repo", type=Path, help="the paper repository's folder")
    ap.add_argument("--dry-run", action="store_true", help="download and hash, copy nothing")
    args = ap.parse_args()

    meta = metadata(args.arxiv_id)
    lic = licence(meta["version_id"])
    meta["licence"] = lic
    meta["redistributable"] = bool(lic and any(k in lic for k in REDISTRIBUTABLE))
    surname = re.sub(r"[^a-z]", "", meta["authors"][0].split()[-1].lower())
    year = meta["first_version"][:4]
    meta["key"] = f"{surname}{year}{slug(meta['title'], 2).replace('-', '')}"
    name = f"{surname}{year}-{slug(meta['title'])}-arXiv-{meta['version_id']}.pdf"

    # The download is untrusted: its own empty directory, never executed.
    with tempfile.TemporaryDirectory(prefix="arxiv_") as tmp:
        pdf = Path(tmp) / "paper.pdf"
        pdf.write_bytes(get(f"https://arxiv.org/pdf/{meta['version_id']}"))
        data = pdf.read_bytes()
        if not data.startswith(b"%PDF-"):
            sys.exit("the download is not a PDF")
        meta["sha256"] = hashlib.sha256(data).hexdigest()
        meta["bytes"] = len(data)
        if meta["redistributable"] and not args.dry_run:
            dest = args.paper_repo / "related-work" / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(pdf, dest)
            meta["pdf"] = f"related-work/{name}"
        else:
            meta["pdf"] = None
            meta["pdf_name_if_kept"] = f"related-work/{name}"
    print(json.dumps(meta, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
