# God-Mode SEO

21 Claude skills for SEO, in 5 departments: Analysis, Optimization, Content, Diagnostics and Strategy.
Each skill does one job, and they all read the same live data through the Distribb SEO connector:
your Google Search Console, real keyword volumes, your backlinks and where AI answers cite you.

Type a skill's name in Claude and it runs. For example:

- `gsc-auditor`: Claude tells you why your clicks dropped, page by page.
- `cannibalization-finder`: it finds the pages fighting each other for the same search.
- `ctr-booster`: it rewrites the titles people see on Google but never click.
- `content-engine`: it writes the article and publishes it straight to your site.

Nothing on your live site changes until you approve the exact edit in chat.

## 1. Connect the data (once)

1. In Claude: **Settings > Connectors > Browse connectors**, search **SEO**, and connect **Distribb**.
2. In Distribb, connect **Google Search Console** and your website. The skills will send you the link if either is missing.
3. Want backlinks on autopilot? Join Distribb's backlink exchange (ask Claude to run `backlink-analyzer`, or switch it on in Distribb). Every article you publish then carries links to partner businesses and earns links back.

## 2. Install the skills

**Claude.ai and the Claude apps:** download [god-mode-seo.zip](https://github.com/Bomx/god-mode-seo/raw/main/dist/god-mode-seo.zip) and upload it in **Settings > Capabilities > Skills > Upload skill**. That one upload holds all 21 skills.

**Claude Code**, any of:

```bash
npx skills add Bomx/god-mode-seo
```

```text
/plugin marketplace add Bomx/god-mode-seo
/plugin install god-mode-seo@god-mode-seo
```

Or copy the folders in `skills/` into `~/.claude/skills/` and type `/gsc-auditor`, `/ctr-booster` and so on.

## The 21 skills

<!-- MENU -->
| # | Skill | Department | What it does |
|---|---|---|---|
| 01 | [`gsc-auditor`](skills/gsc-auditor/SKILL.md) | Analysis | Why your clicks dropped |
| 02 | [`competitor-radar`](skills/competitor-radar/SKILL.md) | Analysis | Your closest rivals, week by week |
| 03 | [`keyword-finder`](skills/keyword-finder/SKILL.md) | Analysis | Volume, difficulty and fit |
| 04 | [`backlink-analyzer`](skills/backlink-analyzer/SKILL.md) | Analysis | The links worth copying |
| 05 | [`mention-tracker`](skills/mention-tracker/SKILL.md) | Analysis | Where AI cites you, and where not |
| 06 | [`meta-optimizer`](skills/meta-optimizer/SKILL.md) | Optimization | Titles that earn the click |
| 07 | [`internal-linker`](skills/internal-linker/SKILL.md) | Optimization | Links between your own pages |
| 08 | [`schema-generator`](skills/schema-generator/SKILL.md) | Optimization | Rich result markup, ready to paste |
| 09 | [`on-page-fixer`](skills/on-page-fixer/SKILL.md) | Optimization | Exact edits, page by page |
| 10 | [`vitals-fixer`](skills/vitals-fixer/SKILL.md) | Optimization | The speed fix to ship first |
| 11 | [`content-engine`](skills/content-engine/SKILL.md) | Content | Brief, article, published |
| 12 | [`content-gap`](skills/content-gap/SKILL.md) | Content | What rivals cover and you skip |
| 13 | [`refresh-finder`](skills/refresh-finder/SKILL.md) | Content | Posts losing clicks, and the fix |
| 14 | [`cluster-builder`](skills/cluster-builder/SKILL.md) | Content | A pillar and its supporting posts |
| 15 | [`geo-optimizer`](skills/geo-optimizer/SKILL.md) | Content | Passages AI answers can quote |
| 16 | [`cannibalization-finder`](skills/cannibalization-finder/SKILL.md) | Diagnostics | Pages fighting for one search |
| 17 | [`robots-checker`](skills/robots-checker/SKILL.md) | Diagnostics | Robots, canonicals, sitemap |
| 18 | [`indexation-doctor`](skills/indexation-doctor/SKILL.md) | Diagnostics | Pages Google never indexed |
| 19 | [`strategy-roadmap`](skills/strategy-roadmap/SKILL.md) | Strategy | Quick wins to long term |
| 20 | [`ctr-booster`](skills/ctr-booster/SKILL.md) | Strategy | Seen a lot, clicked a little |
| 21 | [`kpi-monitor`](skills/kpi-monitor/SKILL.md) | Strategy | Weekly winners and losers |
<!-- /MENU -->

## How they work

- Every number comes from a tool call in your conversation: Search Console, keyword research, backlinks, AI visibility. No estimated volumes, no made-up rankings.
- Diagnose first, then fix: most skills end with the next one or two skills to run.
- Edits to your site go through Distribb (`update_article`, Distribb's own optimizations with their before and after) and only after your yes. Pages Distribb does not manage get the exact copy to paste.
- Skills that need a live page, robots.txt, a sitemap or Google results use Claude's web fetch and web search. Speed checks use Google PageSpeed Insights.

## Build from source

The skills are written once in `src/` (`skills.md` plus the shared `rules.md`). `python3 build.py` writes `skills/`, the plugin manifests in `.claude-plugin/` and `dist/god-mode-seo.zip`.
