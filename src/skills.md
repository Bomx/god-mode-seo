=== gsc-auditor | Analysis | Why your clicks dropped
description: God-Mode SEO, Analysis. Finds why your Google Search Console clicks dropped. Compares the last 28 days with the 28 before, page by page and query by query, and names the cause of each loss (lower rankings, less demand, or fewer people clicking). Use when the user types gsc-auditor or /gsc-auditor, or asks why their clicks, traffic or impressions dropped.
---
# gsc-auditor: why your clicks dropped

## Steps
1. Pick the project and check `setup.search_console.connected` with `get_project`. If it is not connected, send the connect link from `integrations_catalog` and stop.
2. Call `search_console_performance` twice: `days: 28, limit: 100` and `days: 56, limit: 100`. Ask the user first if they want another window (for example 7 vs 7 after an update).
3. Build the previous 28 days with the two-call calculation (cheat sheet) for the totals, every page and every query.
4. Clean the page list (drop or merge `#` and `?` URLs). Split the queries into brand and non-brand (`is_brand` only works on queries). A drop in brand searches is a demand problem, not an SEO one.
5. Rank pages by clicks lost, counting only pages with 100+ impressions in the previous period. For the top 10, name the cause with these rules:
   - **Ranking loss:** average position got worse by 1.5 or more.
   - **Less demand:** impressions down 20% or more while position moved less than 1. Fewer people searched, or a search feature took the space.
   - **Fewer clicks:** impressions within 20% and position within 1, CTR down. The result looks less clickable, or an AI Overview or other feature now sits above it.
   - **Mix shift:** impressions up 20% or more while CTR fell. The page now shows for broader, lower-intent searches: often not a real loss, say so.
   - **Gone:** the page is in the current list with 0 clicks, or missing from it. Check it still returns 200 and is indexable (indexation-doctor).
   - **Unclear:** none of the above. Say so rather than forcing a cause.
6. Do the same for the top 10 queries by clicks lost.
7. Call `list_optimizations` (`limit: 25`) and mark any page Distribb already flagged as `declining_page` or `cannibalisation` (match on `trigger_snapshot.article_url`), with its `signals.why` and the date it was flagged.

## Output
- One sentence: total clicks before and after with the % change, and how much of the loss sits in the top 3 pages.
- Table: page | clicks before > now | impressions before > now | position before > now | cause.
- Next actions, for example: refresh-finder for ranking losses, ctr-booster for click losses, cannibalization-finder when two pages share a query, indexation-doctor for gone pages.

=== competitor-radar | Analysis | Your closest rivals, week by week
description: God-Mode SEO, Analysis. Tracks your closest rivals on the searches that matter to you and on AI answers, as a snapshot you can compare week by week. Use when the user types competitor-radar or /competitor-radar, or asks who outranks them, how competitors are doing, or what changed with rivals.
---
# competitor-radar: your closest rivals, week by week

## Steps
1. Read the rivals from `get_project` (`settings.competitors`). If there are none, ask for 3 to 5 competitor domains.
2. Pick the searches: from `search_console_performance` (`days: 28, limit: 200`) take the 10 non-brand queries with the most impressions where the user ranks in the top 30.
3. For each query, run a live web search and record the position of the user's domain and of each rival in the top 10 (write "not in top 10" when absent). Note the country you searched from: results change by location.
4. Call `ai_visibility_report` with `view: competitors` for citations in AI answers: you, each rival, and the other domains AI leans on.
5. Compare with the last snapshot:
   - In Claude Code, read and write `seo-snapshots/competitor-radar-YYYY-MM-DD.md` in the project folder.
   - In Claude.ai, ask the user to paste last week's table, and end with this week's table in a block they can save.

## Output
- One sentence: who gained and who lost since the last snapshot (or "first snapshot" when there is none).
- Table: query | you | rival 1 | rival 2 | ... with arrows for changes.
- AI citations: you vs each rival.
- Next actions: content-gap on the queries where a rival outranks you, mention-tracker for the AI side.

=== keyword-finder | Analysis | Volume, difficulty and fit
description: God-Mode SEO, Analysis. Finds the keywords worth targeting next, scored by real search volume, keyword difficulty and fit with what the business sells, and checks which ones you already have a page for. Use when the user types keyword-finder or /keyword-finder, or asks for keyword ideas, keyword opportunities or what to write next.
---
# keyword-finder: volume, difficulty and fit

## Steps
1. Read `get_project`: business description, target audience, content pillars, location. Pick 3 to 5 seed keywords from what the business sells (ask the user to confirm them in one line).
2. Call `keyword_research` for each seed with `limit: 30`.
3. Add the queries the site already almost ranks for: from `search_console_performance` (`days: 28, limit: 100`), queries at position 4 to 20 with 10 or more impressions.
4. Remove duplicates. For each candidate, check coverage with `list_articles` (status Published and Planned): does a page or planned article already target it?
5. Label intent and fit for each keyword, buying intent first: comparisons ("x vs y", "alternatives to x"), "best x for y", pricing, "near me", service and problem searches. Pure "what is" topics only when they support a cluster.
6. Score: fit (high 3, medium 2, low 1) x search volume / (keyword difficulty + 10). Show the formula.

## Output
- One sentence: the best 3 opportunities and why.
- Table (top 15): keyword | volume | difficulty | CPC | intent | fit | existing page | action (new page, or optimize the existing one).
- Next actions: cluster-builder to group them, content-engine to write the first one, on-page-fixer for the ones you already rank for.

=== backlink-analyzer | Analysis | The links worth copying
description: God-Mode SEO, Analysis. Reads the backlinks you already have, finds the patterns that earned them, and shows which pages need links next. Use when the user types backlink-analyzer or /backlink-analyzer, or asks about their backlinks, link profile or which pages to build links to.
---
# backlink-analyzer: the links worth copying

## Steps
1. Call `backlinks_status` (credits, links received, verified, exchange participation) and `list_backlinks` (every verified link: source URL, target URL).
2. Group received links by target page and by source domain. Note which kinds of pages earn links (listicles, statistics pages, guides, tools, the homepage), using the page titles from `list_articles` where they are Distribb articles.
3. Find the pages that need links: from `search_console_performance` (`days: 28, limit: 100`) take pages at position 5 to 20 with the most impressions, and mark the ones with zero or one received link.
4. Check the exchange: if `network_participation` is No, explain that joining the backlink exchange (`update_project` with `backlinks_network: true`) makes every article carry links to partner businesses and earns links back. Turn it on only after the user says yes.

## Output
- One sentence: what earns links on this site and which pages need them most.
- Table: page needing links | position | impressions | links now | best link type to get.
- The pattern worth copying (for example "statistics pages earned 40% of links: publish one per pillar").
- Next actions: content-engine for a link-worthy page, internal-linker to pass existing authority, the exchange switch.

=== mention-tracker | Analysis | Where AI cites you, and where not
description: God-Mode SEO, Analysis. Shows where ChatGPT, Gemini, Perplexity and Google's AI answers cite your brand, where they cite competitors instead, and which sites those answers lean on. Use when the user types mention-tracker or /mention-tracker, or asks about AI visibility, AI citations, brand mentions or being recommended by ChatGPT.
---
# mention-tracker: where AI cites you, and where not

## Steps
1. Call `ai_visibility_report` with `view: summary`. If `has_data` is false, tell the user to run a scan from Distribb's AI visibility page and stop.
2. Call `view: prompts` (page through with `page` and `per_page: 10`) to list every tracked buyer prompt and whether you are cited.
3. Call `view: competitors`: citations for you and each rival, and `other_cited` (the domains AI answers lean on).
4. Call `view: cited_pages` to see which of your pages get cited.
5. For each prompt where you are missing, name the page on your site that should answer it (from `list_articles`), or "no page yet".

## Output
- One sentence: engines citing you out of the total, your share of voice, and the biggest gap.
- Table: prompt | cited? | page that should answer it.
- The 5 domains AI cites most that are not you: these are where to get listed or mentioned (roundups, directories, forums, videos).
- Next actions: geo-optimizer on the pages that should answer, content-engine for prompts with no page, keyword-finder for related searches.

=== meta-optimizer | Optimization | Titles that earn the click
description: God-Mode SEO, Optimization. Writes 3 title and meta description variants for a page that ranks but gets few clicks, built on the searches it already shows up for, and applies the one you pick. Use when the user types meta-optimizer or /meta-optimizer, or asks to rewrite a title tag or meta description.
---
# meta-optimizer: titles that earn the click

## Steps
1. Get the page: the URL the user gives, or the 3 pages with the most impressions that rank in the top 10 and fall under your CTR benchmark (cheat sheet) from `search_console_performance` (`days: 28, limit: 100`).
2. Find its searches: the `top_queries` of any optimization for that page in `list_optimizations`, otherwise the site's top queries that match the page's topic.
3. Read the current title and meta: from `list_articles` (Title, MetaDescription) when it is a Distribb article, otherwise fetch the page.
4. Write 3 variants:
   - **A, query first:** the main search, word for word, at the start.
   - **B, benefit:** what the reader gets, with a number only if it is on the page.
   - **C, answer:** the question the searcher has, and a promise the page keeps.
   Titles 60 characters or fewer, meta descriptions 140 to 155 characters, nothing the page does not deliver.
5. On the user's pick and yes: for a Distribb article, `update_article` with `{title, meta_description, sync: true}`; otherwise give the exact copy to paste in their CMS or SEO plugin.

## Output
- Table: variant | title | characters | meta description.
- Your pick and why, in one line.
- Next action: run kpi-monitor in 14 days to see if the CTR moved.

=== internal-linker | Optimization | Links between your own pages
description: God-Mode SEO, Optimization. Builds a 15-row internal link plan with exact anchors and where each link goes, pointing your own authority at the pages closest to page one, and can apply the links. Use when the user types internal-linker or /internal-linker, or asks for internal links, an internal linking plan or how to link pages together.
---
# internal-linker: links between your own pages

## Steps
1. List the site's pages: `list_articles` with status Published (page through with `offset`), plus the content pillars from `get_project`.
2. Pick the targets: pages with `striking_distance: true` in `search_console_performance` (`days: 28, limit: 100`), plus the content pillars (the pages that sell).
3. For each target, find 2 or 3 source pages on a related topic that do not link to it yet. Check with `get_article` that the target URL is not already in the source's HTML.
4. Choose the anchor from the target's main search (exact or a close variant) and the spot: quote the sentence in the source where the link fits naturally.
5. Also list Distribb's own `internal_link` and `link_boost` optimizations from `list_optimizations`.
6. On yes, apply one link at a time with `update_article` (content with the link added, `sync: true`), showing the changed sentence before and after. Distribb optimizations are applied with `review_optimization` then `publish_optimization`.

## Output
- Table (15 rows): source page | anchor text | target page | the sentence where it goes.
- Next actions: apply the plan, then kpi-monitor in 2 to 4 weeks on the targets.

=== schema-generator | Optimization | Rich result markup, ready to paste
description: God-Mode SEO, Optimization. Writes valid JSON-LD structured data for a page (Article, Product, SoftwareApplication, LocalBusiness, Organization, BreadcrumbList, FAQPage) using only facts that are on the page. Use when the user types schema-generator or /schema-generator, or asks for schema markup, structured data, JSON-LD or rich results.
---
# schema-generator: rich result markup, ready to paste

## Steps
1. Get the page: `get_article` for a Distribb article, otherwise fetch the URL. Read `get_project` for the business name, website and location.
2. Pick the types that match what the page is: BlogPosting or Article for posts, Product or SoftwareApplication for product pages, LocalBusiness (with the address the business gave) for local pages, Organization and WebSite for the homepage, BreadcrumbList when the page has breadcrumbs. Use FAQPage only when the questions and answers are visible on the page, and say that Google shows FAQ rich results mainly for government and health sites.
3. Fill every field from the page or the project. Never add ratings, reviews, prices, dates or authors that are not on the page. Leave out a field rather than invent it.
4. Validate: check the JSON parses, required properties per type are present, and URLs are absolute.

## Output
- The JSON-LD in one `<script type="application/ld+json">` block.
- Where to paste it (theme header, SEO plugin, or the page's custom code), and the test to run: Google's Rich Results Test.
- On yes for a Distribb article, add it with `update_article` (`sync: true`). Some CMSs strip scripts from post content: if so, say to add it through the SEO plugin instead.

=== on-page-fixer | Optimization | Exact edits, page by page
description: God-Mode SEO, Optimization. Audits one page against the searches it ranks for and the pages above it, and returns exact edits (old text, new text), not generic advice. Use when the user types on-page-fixer or /on-page-fixer, or asks to optimize a page, improve a page's rankings or do an on-page SEO audit.
---
# on-page-fixer: exact edits, page by page

## Steps
1. Get the page: the URL the user gives, or the 5 pages with `striking_distance: true` and the most impressions from `search_console_performance`.
2. Its searches: `top_queries` from any `list_optimizations` entry for the page, otherwise the site's top queries on its topic.
3. Read the page (`get_article` or fetch) and the top 3 results for its main search (web search, then fetch).
4. Check, in this order: the main search in the title and H1; the answer in the first two or three sentences; subtopics the top results cover that the page skips; thin or outdated sections (old years, dead tools, old prices); internal links to and from the pillar page; image alt text.
5. Write each fix as old text and new text, with the section it belongs to.
6. If Distribb already has an optimization for this page, show its before and after (`get_optimization`) as the alternative.

## Output
- One sentence: the single biggest reason the page sits where it does.
- Numbered edits: section | old | new | why.
- On yes: `update_article` (`sync: true`) for Distribb articles, or `review_optimization` approve then `publish_optimization`. Otherwise the user pastes the edits.

=== vitals-fixer | Optimization | The speed fix to ship first
description: God-Mode SEO, Optimization. Measures Core Web Vitals (LCP, INP, CLS) on your most visited pages with Google PageSpeed Insights and ranks the fixes, so you ship the one that matters first. Use when the user types vitals-fixer or /vitals-fixer, or asks about Core Web Vitals, page speed, LCP, INP or CLS.
---
# vitals-fixer: the speed fix to ship first

The connector has no speed data, so this skill reads Google's PageSpeed Insights.

## Steps
1. Pick the pages: the 5 pages with the most clicks in `search_console_performance` (`days: 28`).
2. For each, fetch `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<URL>&strategy=mobile&category=performance` (URL-encoded). Without a fetch tool, ask the user to run pagespeed.web.dev and paste the results.
3. Read the field data first (`loadingExperience`: LCP, INP, CLS at the 75th percentile, and its category). Use the lab data (`lighthouseResult.audits` with savings) for the causes. Thresholds for good: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less.
4. Group the causes across pages (for example "hero image not preloaded" on 4 of 5 pages) and rank them by pages affected x the savings PageSpeed reports.
5. Write the fix for the site's platform (from `get_project`, `setup.website.platform`): WordPress, Shopify, Webflow or custom.

## Output
- One sentence: which metric fails, on how many of the 5 pages, and the fix to ship first.
- Table: page | LCP | INP | CLS | status (from field data, or "lab only" when there is none).
- The ranked fix list with the exact steps for their platform.

=== content-engine | Content | Brief, article, published
description: God-Mode SEO, Content. Takes a keyword from research to a published article: checks it is not already covered, reads what ranks, writes the brief and the article, and saves it to your site through Distribb for your approval. Use when the user types content-engine or /content-engine, or asks to write an article, a blog post or a page for a keyword.
---
# content-engine: brief, article, published

## Steps
1. **Check the keyword.** `keyword_research` for volume, difficulty and related searches. Check `list_articles` and `search_console_performance`: if a page already targets or ranks for it, recommend on-page-fixer for that page instead and stop unless the user insists.
2. **Read what ranks.** Web search the keyword and read the top 5. Let the results decide the format: lists rank, write a list; comparisons rank, write a comparison. A named product or brand in the keyword means a listicle or comparison.
3. **Brief.** Title, the answer-first paragraph, H2s that match the questions searchers ask, what you will add that the top results lack (a worked example, real numbers from the business, a clear recommendation), internal links to the content pillar and 2 to 4 related published articles. If it is a planned Distribb article, read `get_article_brief` for the exchange partner links it must carry.
4. **Write.** Full HTML, answer first, specific, short paragraphs, a table where things are compared. No invented statistics, quotes, reviews or prices: leave out anything you cannot source.
5. **Save.** Show the title, meta description and first paragraph, then on yes `create_article` with `keyword`, `title`, `content`, `meta_description` and the `scheduled_date` the user picks. Content of 2,000+ characters is published exactly as sent. To publish right away, `publish_article` after a second yes.
   Or let Distribb write it: `create_article` with only the keyword and a date, and Distribb writes and publishes it on that date.

## Output
- The brief (short), then the article preview, then the saved article and its scheduled date or live URL.

=== content-gap | Content | What rivals cover and you skip
description: God-Mode SEO, Content. Compares your page or site with the pages that rank above you and lists the subtopics and the pages you are missing, with search volumes. Use when the user types content-gap or /content-gap, or asks for a content gap analysis or what competitors cover that they don't.
---
# content-gap: what rivals cover and you skip

## Steps
1. Get the topic: a keyword, or a page of theirs (then its main search from `list_optimizations` or Search Console).
2. Web search it and read the top 5 results: list their H2s, the questions they answer and the entities they name.
3. Read the user's page (`get_article` or fetch) and their other articles' titles (`list_articles`).
4. Two gap lists:
   - **Missing on this page:** subtopics 3 or more of the top 5 cover that the page does not.
   - **Missing pages:** topics the rivals have a whole page on that the site has none for. Check volume with `keyword_research`.
5. If competitors are set in `get_project`, give each gap the rival that covers it best.

## Output
- One sentence: the biggest gap.
- Table 1: subtopic | covered by (how many of the top 5) | where it goes on the page.
- Table 2: missing page | search volume | difficulty | rival with that page.
- Next actions: on-page-fixer for table 1, content-engine for table 2.

=== refresh-finder | Content | Posts losing clicks, and the fix
description: God-Mode SEO, Content. Finds the articles losing clicks month over month and writes the refresh each one needs (new dates, facts, sections and examples), then applies it with your approval. Use when the user types refresh-finder or /refresh-finder, or asks which posts are decaying, losing traffic or need updating.
---
# refresh-finder: posts losing clicks, and the fix

## Steps
1. List Distribb's `declining_page` optimizations from `list_optimizations` with their `signals` (impressions and position before and after).
2. Add your own: the previous-period calculation (cheat sheet) on `search_console_performance` with `days: 28` and `56`, limited to article URLs (from `list_articles`, status Published). A post is decaying when it lost 30% or more of its clicks or slid 2 or more positions.
3. For the top 5 by clicks lost, read the post (`get_article` or fetch) and the current top 3 results for its main search. Find what is stale: old years, outdated prices or tools, a slower answer than the results above it, missing subtopics.
4. Write the refresh as a list of edits (old, new) plus a new intro sentence with the current year only where the content is truly updated.
5. If Distribb has a `declining_page` optimization for the post that passes the stale-rewrite check (ground rules), show its before and after (`get_optimization`); on yes, `review_optimization` with `action: "approve"`, then `publish_optimization` when it is ready. Otherwise on yes, `update_article` with `sync: true`.

## Output
- Table: post | clicks before > now | position before > now | what is stale.
- The edits for each post.

=== cluster-builder | Content | A pillar and its supporting posts
description: God-Mode SEO, Content. Plans a topic cluster around one service: a pillar page and 8 to 12 supporting posts with real search volumes, the links between them, and the articles to schedule. Use when the user types cluster-builder or /cluster-builder, or asks for a topic cluster, a content plan, a pillar page or topical authority.
---
# cluster-builder: a pillar and its supporting posts

## Steps
1. Pick the pillar: a service from `get_project` (content pillars, business description) or the user's topic.
2. `keyword_research` on the pillar seed with `limit: 50`, plus 2 related seeds.
3. Group the keywords by intent: one pillar page (the broad money search) and 8 to 12 supporting posts (comparisons, best-x-for-y, problems, how-tos that lead to the service). Buying intent first.
4. Check coverage with `list_articles` (Published and Planned): mark what exists, what to optimize, what is missing.
5. The link plan: every supporting post links to the pillar with the pillar's main search as anchor; the pillar links to each supporting post; siblings link where the reader needs it.
6. On yes, schedule the missing posts with `create_article` (keyword, title, `scheduled_date` spread over the weeks the user picks). Without content Distribb writes each one on its date.

## Output
- The cluster map: pillar, then each supporting post with keyword | volume | difficulty | status (exists, optimize, missing).
- The link plan.
- The schedule you created, when you created one.

=== geo-optimizer | Content | Passages AI answers can quote
description: God-Mode SEO, Content. Rewrites the passages on your pages that AI assistants and Google's AI answers should quote: answer-first blocks, clear definitions and checkable facts, aimed at the prompts where you are not cited yet. Use when the user types geo-optimizer or /geo-optimizer, or asks about GEO, AEO, generative engine optimization or getting quoted by AI.
---
# geo-optimizer: passages AI answers can quote

## Steps
1. Find the prompts to win: `ai_visibility_report` with `view: prompts`, the ones where you are not cited. Add Distribb's `conversational_query` and `answer_gap` optimizations from `list_optimizations`.
2. For each, pick the page that should answer it (`list_articles`, the cited pages from `view: cited_pages`), and read it.
3. Write a quotable block for each prompt:
   - The question as an H2 or H3, in the words people use.
   - A 40 to 60 word answer that stands on its own and names the business where it is honest to.
   - One specific, checkable fact from the page or the business (a price, a number, a place, a time).
   - A short list or table when the answer is a comparison or steps.
4. Keep facts about the business the same everywhere (name, what it does, prices, locations).
5. On yes: `update_article` (`sync: true`) with the block inserted where shown, or approve Distribb's matching optimization (`review_optimization`, then `publish_optimization`).

## Output
- Table: prompt | page | the block (preview).
- Next action: re-run mention-tracker after the next AI visibility scan.

=== cannibalization-finder | Diagnostics | Pages fighting for one search
description: God-Mode SEO, Diagnostics. Finds the pages on your site competing for the same Google search, picks the one that should win, and fixes the others (merge, redirect, re-angle or link). Use when the user types cannibalization-finder or /cannibalization-finder, or asks about keyword cannibalization or pages competing with each other.
---
# cannibalization-finder: pages fighting for one search

## Steps
1. Call `list_optimizations` (`limit: 25`) and keep suggestions with `opportunity_type: cannibalisation` that are not rejected. For each, `get_optimization` gives the query, the competing pages with their Search Console data, and the page Distribb picked to win. Advisory rows carry no rewrite: you fix those yourself. Ignore conflicts about search operators (queries starting with `site:` and similar).
2. Add likely conflicts Distribb has not flagged: articles in `list_articles` (MainKeyword, Title) with the same or nearly the same main keyword. On big sites, check the keywords behind the site's top non-brand queries first rather than every article. Fetch each losing URL: if it already redirects to the winner, it is fixed; drop it. Treat the rest as "to check", not proven.
3. For each conflict, choose the winner by clicks and position from `search_console_performance` (`days: 28, limit: 100`; a page missing from that list has fewer clicks than every page in it), then by which page matches the search intent.
4. Pick the fix for each loser:
   - **Same intent, weaker page:** merge its useful parts into the winner, then a 301 redirect from loser to winner. Give the exact rule for their CMS (`get_project`, `setup.website.platform`); when it is unknown, ask, or give the WordPress, Shopify and Webflow versions.
   - **Different intent possible:** re-angle the loser to its own search (new title, H1 and intro).
   - **Both needed:** keep both, link loser to winner with the query as anchor, and remove the query from the loser's title.
5. On yes, apply the edits you showed with `update_article`, or Distribb's re-angle when it passes the stale-rewrite check.

## Output
- Table: search | winner | loser(s) | fix.
- The exact redirect rules or edits.

=== robots-checker | Diagnostics | Robots, canonicals, sitemap
description: God-Mode SEO, Diagnostics. Checks robots.txt, the XML sitemap, canonical tags and noindex tags against your most important pages, and returns a deploy-ready fix. Use when the user types robots-checker or /robots-checker, or asks to check robots.txt, the sitemap, canonicals or noindex.
---
# robots-checker: robots, canonicals, sitemap

## Steps
1. Fetch `https://<site>/robots.txt` (site from `get_project`). Without a fetch tool, ask the user to paste it.
2. List every Disallow rule and test the 20 pages with the most clicks (`search_console_performance`, `days: 28`) against them. Any important page blocked is a critical issue.
3. Find the sitemap (`sitemap_url` from `get_project`, or the Sitemap line in robots.txt). Fetch it (and its child sitemaps). Check the 20 top pages are listed, and fetch up to 20 sitemap URLs to confirm they return 200 and are not redirects or noindex.
4. Fetch the 10 top pages and read the canonical tag (should point to itself unless on purpose) and any meta robots noindex.

## Output
- One sentence: critical issues first, or "no blocking issues".
- Table: check | result | pages affected | fix.
- A corrected robots.txt as a diff when rules need changing, and the exact tag changes for canonicals.

=== indexation-doctor | Diagnostics | Pages Google never indexed
description: God-Mode SEO, Diagnostics. Finds published pages that get no Google impressions at all, works out why (noindex, wrong canonical, missing from the sitemap, no internal links, thin content), and lists the fix for each. Use when the user types indexation-doctor or /indexation-doctor, or asks about pages not indexed, crawled but not indexed, or pages with no traffic.
---
# indexation-doctor: pages Google never indexed

## Steps
1. All published URLs: `list_articles` with status Published (page through with `offset`).
2. Pages Google shows: `search_console_performance` with `days: 90, limit: 100`. A published page older than 3 weeks that is not in that list has little or no Google visibility: it is either not indexed or indexed and invisible. Say "not in the top 250 pages" rather than "zero impressions" on large sites.
3. Add Distribb's `crawl_proxy` optimizations from `list_optimizations` (pages with impressions but almost no clicks).
4. For up to 20 pages, oldest first, fetch each and check: noindex, canonical pointing elsewhere, redirects, in the sitemap or not, linked from any other article (search the HTML of the related articles with `get_article`), and thin content (under 300 words).
5. Say plainly that only Search Console's URL Inspection confirms indexing: ask the user to inspect the top 3 and request indexing after the fixes.

## Output
- Table: page | published | likely cause | fix.
- Next actions: internal-linker for orphans, robots-checker when several pages share the same block, refresh-finder for thin pages.

=== strategy-roadmap | Strategy | Quick wins to long term
description: God-Mode SEO, Strategy. Builds an SEO roadmap from your own data: quick wins for this week, the work for this quarter, and the long-term moves, each tied to the skill that does it. Use when the user types strategy-roadmap or /strategy-roadmap, or asks for an SEO strategy, plan or roadmap.
---
# strategy-roadmap: quick wins to long term

## Steps
1. Gather (keep it to these calls): `get_project`; `search_console_performance` with `days: 28` and `56`; `list_optimizations` (pending and ready); `keyword_research` on the main service; `backlinks_status`; `ai_visibility_report` summary.
2. Find the wins:
   - **This week:** optimizations already ready to publish, striking-distance pages (position 4 to 20 with impressions), low-CTR titles (your CTR benchmark).
   - **This quarter:** clusters to build around the money pages, decaying posts to refresh, cannibalization to fix, prompts where AI cites rivals instead.
   - **Long term:** authority (the backlink exchange, getting onto the "best x" roundups AI reads, a statistics page per pillar), technical health.
3. For each item: the data that justifies it, the skill to run, effort (S, M, L).

## Output
- One sentence: the one thing to do first and why.
- Three tables (this week, this quarter, long term): action | why (data) | skill | effort. 12 items at most in total.

=== ctr-booster | Strategy | Seen a lot, clicked a little
description: God-Mode SEO, Strategy. Finds the pages and searches with many Google impressions but few clicks, rewrites their titles and descriptions, and publishes the rewrite with your approval. Use when the user types ctr-booster or /ctr-booster, or asks to improve click-through rate or get more clicks from the same rankings.
---
# ctr-booster: seen a lot, clicked a little

## Steps
1. `search_console_performance` with `days: 28, limit: 100`. Build your CTR benchmark by position band (cheat sheet).
2. Keep pages and queries in the top 10 with 100+ impressions and a CTR under half of their band's median (brand queries out). Add Distribb's `ctr_underperform` and `query_segment` optimizations from `list_optimizations` (`status: pending`, `limit: 25`). Note that searches with zero clicks never appear in `top_queries`, so the list under-counts.
3. Rank them by missed clicks = impressions x (band median CTR - their CTR). Label this an estimate from the site's own data.
4. For the top 10: read the current title and meta (from `list_articles`: Title, MetaDescription, MainKeyword; fetch the page when it is not a Distribb article). The connector does not link pages to queries: use the optimization's `top_queries` when there is one, otherwise the page's main keyword, and say which you used. Write one rewrite each, built on that search (60 characters for titles, 140 to 155 for descriptions, nothing the page does not deliver). Use meta-optimizer when the user wants 3 variants.
5. On yes, apply the exact title and meta the user saw: `update_article` with `{title, meta_description, sync: true}` for Distribb articles, otherwise the copy to paste. Use Distribb's own optimization only when it passes the stale-rewrite check (ground rules) and you showed its proposed title and meta.

## Output
- Table: page | main search | impressions | CTR vs band median | estimated missed clicks | new title.
- What you changed, and a reminder to run kpi-monitor in 14 days.

=== kpi-monitor | Strategy | Weekly winners and losers
description: God-Mode SEO, Strategy. A weekly SEO report from live data: clicks, impressions, position, the pages and searches that won and lost, new backlinks, AI visibility and what was published. Use when the user types kpi-monitor or /kpi-monitor, or asks for a weekly SEO report, KPIs or how SEO did this week.
---
# kpi-monitor: weekly winners and losers

## Steps
1. `search_console_performance` with `days: 7` and `days: 14` (limit 1000). Previous week by the two-call calculation. Say the last 2 to 3 days are incomplete.
2. Totals: clicks, impressions, CTR, position, this week vs last.
3. The 5 pages and 5 searches that gained the most clicks, and the 5 that lost the most.
4. `backlinks_status` (links received and verified) and `ai_visibility_report` summary (score, engines citing you). To show change, compare with last week's report: in Claude Code read and write `seo-snapshots/kpi-monitor-YYYY-MM-DD.md`; in Claude.ai ask the user to paste last week's numbers.
5. What shipped: `list_articles` with status Published and `scheduled_after` a week ago, and optimizations published this week from `list_optimizations`.

## Output
- One sentence: the week in numbers and its biggest mover.
- KPI table: metric | this week | last week | change.
- Winners and losers tables, then what shipped.
- Offer to run it every Monday (Claude Code: a scheduled task; Claude.ai: ask each week).
