---
name: related-work
description: Add a related paper to a FASTENER paper repository (papers/P<n> - <title>/, its own public GitHub repo) -- fetch its metadata and licence, keep the PDF in related-work/ only if the licence allows redistribution, and write its entry in BIBLIOGRAPHY.md (reference, link, hash, licence, what it does, how it relates to the paper, BibTeX); then commit and push that paper repo. Use when the user gives an arXiv link, DOI or paper title and asks to add it to a paper's related work, literature, references or bibliography (P1-P10), or to collect, note or file a paper for one of the planned papers.
---

# Related work for a paper repository

Each potential paper (P1-P10) is its own public repository, cloned into
`papers/P<n> - <title>/` and listed in `papers/README.md`. Its related work
lives in two places:

- `related-work/` -- the PDFs, **only** where the licence allows anyone to
  redistribute them (the repositories are public);
- `BIBLIOGRAPHY.md` -- one entry per paper, whether or not its PDF is kept.

Interpreter: `C:\Users\klemen\.conda\envs\fastener-exp\python.exe`. First
example: P5 and Silvestri et al. 2025 (arXiv:2510.20351).

## 1. Fetch

For an arXiv paper:

```
python -I .claude/skills/related-work/fetch_arxiv.py <arXiv id> "papers/P<n> - <title>"
```

It reads the arXiv API and the abstract page's licence and downloads the
latest version (or the one given, `2510.20351v2`) into a fresh temporary
directory. It checks the file is a PDF and hashes it. It copies the PDF to
`related-work/<surname><year>-<title-slug>-arXiv-<id>v<k>.pdf` only for CC BY,
CC BY-SA or CC0. It prints a JSON record (metadata, abstract, licence,
SHA-256, a citation key) for step 2. `--dry-run` copies nothing.

- **The arXiv default licence (non-exclusive distribution licence) or no
  licence:** the PDF is not kept. The entry links to arXiv. Say so to the user.
- **Not on arXiv** (a DOI or publisher page): read the publisher page for the
  metadata and the licence, download only an open-access PDF whose licence
  allows redistribution, and hash it the same way. Never keep a paywalled
  PDF, and never use a PDF from a shadow library.
- A download is untrusted data: never open it with anything that executes it.

## 2. Write the BIBLIOGRAPHY.md entry

Create the file if it is missing. Its head:

```
# Bibliography

Related work for P<n>. PDFs are kept in [related-work/](related-work/) only where the licence allows redistribution.
```

Then one section per paper, newest addition last:

```
## <First author surname> et al. (<year>) -- <short title>

<All authors.>
*<Full title.>*
arXiv:<id> (<category>), first version <date>; v<k> kept here.   # or: venue, volume, pages, DOI
<https://arxiv.org/abs/<id>> -- PDF: [related-work/<file>](related-work/<file>)
(SHA-256 `<hash>`). Licence: <licence>.                           # or: "PDF not kept: <licence>."

**What it does** (from the abstract): <three to five sentences, in our words>.

**Relevance to P<n>.** <How it relates to this paper's experiments
(H-numbers, the claim, the method). What overlaps and what differs. What
still has to be read or compared before the manuscript.>

```bibtex
@misc{<key>, ...}            # @article / @inproceedings once published
```
```

Rules:

- **Say how deeply it was read.** "From the abstract" when only the abstract
  was read. Claim nothing about the method, datasets or results beyond what
  was actually read.
- **The relevance paragraph** names the paper's own experiments and says
  what still has to be checked. Do not call our work "the first" or "novel"
  from one entry.
- **Keep names and keys stable.** If a PDF or BibTeX key is already
  committed, keep it; the script's suggestion is for new entries.
- **Link from the README.** The paper's README links `BIBLIOGRAPHY.md` and
  `related-work/` once, on the line before the experiments link.

## 3. Commit and push the paper repository

In the paper's folder, not in fastener-experiments, which ignores
`papers/P*/`:

```
git add BIBLIOGRAPHY.md related-work README.md
git commit -m "Related work: <surname> et al. <year>, <short title> (arXiv:<id>v<k>, <licence>), PDF and BIBLIOGRAPHY.md"
git push
```

- Commit as Klemen Kenda only, with no co-author line.
- The P2 folder is owned by another Windows user, so there use
  `git -c safe.directory=* ...` (`gh` refuses that folder; `git push` works).

## 4. Tell the user

One line each:
- what was added and where;
- whether the PDF was kept, and its licence;
- how deeply it was read;
- the one sentence on how it relates to the paper;
- the repository link.
