# Liuyuan Jiang — The geometry of learning and decisions

A separate static research website with seven project pages with integrated explanations, interactive teaching diagrams, and seven separate video pages with narration/storyboard downloads. The recorded videos are not included.

## Preview

Run `python3 -m http.server 8765 --bind 127.0.0.1 --directory dist` from this folder, then open http://127.0.0.1:8765/.

## Edit

- `content/papers.json`: author order, titles, venues, links, and source records.
- `content/articles.json`: integrated project explanations, evidence, and narration scenes.
- `content/explanations/`: editable Markdown exports of the explanations.
- Old `/blog/` URLs redirect to the matching project page and are excluded from the sitemap.
- `/videos/<paper>/`: separate video pages. Narration and storyboards appear here, not on project pages.
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

Each file in `video-scripts/` contains narration plus on-screen directions. Record the narration, add paper figures with their table/figure identifiers, include captions, and end with the project URL. After uploading a video, add its verified embed URL to the corresponding video page. Do not label a script as a recorded talk.

## Refined project narratives

`content/project-stories.json` controls each paper’s human-readable headline, hero figure captions, three-step method, technical reasoning, notation, result context, measured chart values, and connections to other papers. `content/articles.json` holds the integrated explanation and video scenes. Measured charts cite their specific table or section. Interactive geometry and bound envelopes are clearly labeled as toy or schematic.

The project pages contain explanations, interactive examples, results, technical details, and citations. Narration and storyboards live at `/videos/<slug>/`; these are production drafts, with no recorded videos yet. Legacy `/blog/<slug>/` URLs redirect to the integrated explanation.

## Mathematical notation and research areas

The hub opens with an interactive direction explorer: Multi-objective Learning (SURF), Bilevel Optimization (four papers), and Applications (RetailAgent and BiRQ). The direction labels do not fix a permanent number of research areas. `research_hub.py` controls the topic map and publication rows. The rows show each paper’s full title, authors, venue, figure preview, and available resource links. Preview plots are labeled as illustrative or linked to their primary-paper table.

`content/equations.json` contains the display and inline TeX. `compile_math.mjs` renders it with the pinned, locally vendored KaTeX 0.19.0 package; `math_typesetting.py` adds accessible MathML and bundles the local stylesheet and fonts. `python3 build.py` requires Node.js (uses the installed Codex runtime as a fallback on this computer). Equations are pre-rendered and do not depend on a CDN or browser JavaScript. Malformed TeX fails the build. Main formulations, interactive constraint-regime formulas, and update steps use the same renderer.

### Research atlas and original paper figures

SURF is pinned first at the author’s request. Remaining publications are sorted by publication year, newest first; first public release month breaks ties within a year. `content/hub-curation.json` records this ordering, descriptive paper-jump labels, and the paper-to-visual evidence notes. Direction links include the paper’s contribution and venue and jump to stable `#paper-<slug>` publication anchors.

The opening headline is “The geometry of learning and decisions.” The direction tabs support clicks, arrow keys, Home/End, and direct direction fragments. The multi-objective example contrasts equally spaced scalarization weights with equal arc-length spacing on the exact toy front `(z², (1−z)⁴)`. The bilevel example lets readers move a constraint in a labeled toy response problem. Applications switches between original BiRQ and RetailAgent architecture figures. With JavaScript disabled, all directions remain available.

`content/paper-figures.json` records each original figure or table, its source URL, local image dimensions, explanatory caption, and any PDF crop. Original artwork lives in `dist/assets/paper-figures/`. arXiv PNG/SVG assets are preserved; RetailAgent Figure 2 and EUSIPCO Table I are extracted from the original PDFs. The project page displays a source link and full-size image link for every figure. Preview charts for RetailAgent and smoothness are explicitly distinguished as reported results and an explanatory toy.
