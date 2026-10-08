# Liuyuan Jiang — Research, explained

A separate static research website with seven project pages, seven blog explainers, interactive teaching diagrams, and narration/storyboard downloads. The recorded videos are not included.

## Preview

Run `python3 -m http.server 8765 --bind 127.0.0.1 --directory dist` from this folder, then open http://127.0.0.1:8765/.

## Edit

- `content/papers.json`: author order, titles, venues, links, and source records.
- `content/articles.json`: project explanations, blog prose, evidence, and narration scenes.
- `dist/assets/style.css`: responsive visual design.
- `dist/assets/site.js`: interactive educational diagrams.
- `build.py` and `render_articles.py`: generate static pages and editable Markdown exports.

Run `python3 build.py` after editing content. No npm dependencies or build service are required.

## Publication inventory

1. SURF — NeurIPS 2026 acceptance reported on the author’s homepage. Public arXiv manuscript from May 2026.
2. RetailAgent — 2026 preprint. No conference acceptance is asserted.
3. BiRQ — ICASSP 2026 acceptance reported on the author’s homepage. Public arXiv manuscript from September 2025.
4. Efficient Penalty-Based Bilevel Methods — 2025 preprint. Related to the preceding Beyond Value Functions work; kept as a separate public record.
5. Beyond Value Functions / PBGD-Free — NeurIPS 2025.
6. Improved Analysis of Penalty-Based Methods — EUSIPCO 2025.
7. BLOCC — NeurIPS 2024.

The inventory covers publicly discoverable papers checked on October 8, 2026. It does not assert completeness for unpublished work or newly indexed records.

## Research content

Primary paper links are included on every project and explainer page. Code links are included where an author repository was verified. Venue announcements with only author-page verification are labeled accordingly. The website follows the progression of the advisor’s reference: takeaway, explanation, interactive concept, supporting evidence, technical scope, and citation. Its source and design were written independently.

All toy demonstrations identify their status. The BiRQ WER chart uses measured values from Table 2. The timing widget uses synthetic returns. The schedule widget is a teaching illustration and is not a runtime benchmark. Narration scripts include on-screen directions and recording notes.

## Files and hosting

Everything created for this project stays in this folder. `work/` holds downloaded public PDFs, extraction files, temporary publishing files, and QA artifacts. It is excluded from the source repository and deployment archive. The deployed static files are in `dist/`. The hosting identity is in `.openai/hosting.json`.

The initial hosted version is private for review. Public visibility requires changing its audience. To move to another static host later, upload `dist/`, change the origin in `content/site.json`, and regenerate pages so canonical links and the sitemap match the new address.

## Recording the videos

Each file in `video-scripts/` contains narration plus on-screen directions. Record the narration, add paper figures with their table/figure identifiers, include captions, and end with the project URL. After uploading a video, add its verified embed URL to the corresponding project page. Do not label a script as a recorded talk.
