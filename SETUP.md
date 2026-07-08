# Setup & Customization Guide

This README is designed to live in a special repository: one whose name
**exactly matches your GitHub username** (e.g. `github.com/jhonsnow456/jhonsnow456`).
That's the only repo type GitHub renders as your profile page.

---

## 1. Folder structure

```
jhonsnow456/                       ← repo name MUST equal your username
├── README.md                      ← the profile page itself
├── assets/
│   ├── README.md
│   └── rpg-stats.json             ← generated, do not hand-edit
├── scripts/
│   └── compute_rpg_stats.py       ← XP / achievements engine
├── .github/
│   └── workflows/
│       ├── snake.yml              ← contribution snake animation
│       └── update-readme.yml      ← quest log, blog feed, RPG stats
└── docs/
    └── SETUP.md                   ← this file
```

---

## 2. Installation

1. Create a new **public** repository named exactly your GitHub username.
2. Copy every file from this deliverable into that repo, preserving paths.
3. Commit and push to `main`.
4. Enable Actions: repo → **Settings → Actions → General → Allow all actions**.
5. Within a few minutes of the first push, `snake.yml` runs and creates an
   `output` branch containing the generated snake SVGs. Nothing to do here
   manually — the workflow creates that branch itself.
6. Edit the placeholder links (`your-portfolio-url.com`, `linkedin.com/in/your-handle`,
   feed URLs, etc.) throughout `README.md`.

---

## 3. Required tokens & secrets

| Secret name | Used by | Scopes needed | Notes |
|---|---|---|---|
| `RM_TOKEN` | `update-readme.yml` (quest log + RPG script) | `public_repo`, `read:user` | A **classic Personal Access Token**, not the default `GITHUB_TOKEN` — the activity/quest-log action and cross-API search calls need a token tied to your account, not the repo-scoped default. |
| `GITHUB_TOKEN` | `snake.yml` | auto-provided by Actions | No setup needed; make sure the repo's Actions have **write** permission (Settings → Actions → General → Workflow permissions → Read and write). |

To add `RM_TOKEN`:
1. GitHub → Settings → Developer settings → Personal access tokens →
   Tokens (classic) → Generate new token, scopes `public_repo` + `read:user`.
2. In your profile repo: Settings → Secrets and variables → Actions →
   New repository secret → name it `RM_TOKEN`, paste the value.

---

## 4. Customization guide

- **Colors/theme**: every stats widget below takes `theme=` or explicit
  `title_color` / `bg_color` / `icon_color` query params. Swap `tokyonight`
  for `dracula`, `radical`, `synthwave`, etc. if you don't want the
  cyan-on-navy cyberpunk palette.
- **Skill Tree bars**: hand-edit the percentages in the Skill Tree table —
  these are intentionally not auto-generated since "skill %" isn't a real
  metric any API exposes. Keep them honest; recruiters notice inflated bars.
- **Tech Arsenal badges**: trim to tools you actually use. More isn't better
  here — a focused 20-badge arsenal reads stronger than 60.
- **RPG XP formula**: edit the weights directly in
  `scripts/compute_rpg_stats.py::compute_xp`. The current formula is a
  reasonable default, not gospel.
- **Achievements thresholds**: same file, `compute_achievements`. Add your
  own conditions (e.g. hackathon wins) as extra boolean flags, then add a
  matching row in the README table.
- **Blog feed**: replace the two feed URLs in `update-readme.yml` under
  `feed_list` with your actual Dev.to/Medium/Hashnode RSS URLs. Remove the
  ones you don't use.
- **Snake animation**: if you fork/rename the repo, update the two
  `raw.githubusercontent.com/.../output/...` URLs in the README's
  "GitHub Analytics Room" section to match your new username/repo.

---

## 5. Graceful degradation

Every dynamic section is designed to fail safely:

- If `RM_TOKEN` is missing or expired, `update-readme.yml` fails on just
  that step — the README keeps its last successfully-synced content rather
  than showing an error.
- If a third-party stats service (github-readme-stats, streak-stats, etc.)
  is down, the `<img>` tag simply renders as a broken image icon in that one
  card — it does not break the rest of the page. If you see broken badges
  for more than a day, check https://github-readme-stats.vercel.app/api/status
  or self-host the service (see below).
- LeetCode/Codeforces/etc. are static link badges, not live widgets, by
  design — free third-party "stat card" services for these platforms are
  unreliable and rotate frequently. Swapping in a live one later is a
  drop-in change (replace the badge line with an `<img>` pointing at
  whichever service you choose).

---

## 6. Optional premium enhancements

- **Self-host github-readme-stats**: fork the repo, deploy to Vercel with
  your own token, and point the `<img>` URLs at your instance. Removes
  rate-limit risk from the shared public instance entirely.
- **WakaTime integration**: if you install the WakaTime CLI plugin in your
  editor, `github-readme-stats` can render a weekly coding-activity card
  automatically once your WakaTime API key is added as a secret
  (`WAKATIME_API_KEY`) — add:
  `![WakaTime](https://github-readme-stats.vercel.app/api/wakatime?username=jhonsnow456)`
- **LeetCode live card**: services like `leetcode-stats-card` (community
  Vercel deployments) can replace the static LeetCode badge — verify uptime
  before relying on one, as these are unofficial and occasionally go dark.
- **Spotify "now playing"**: `novatorem/spotify-github-profile` gives a
  live now-playing widget if you want it; requires a Spotify API app +
  refresh token as secrets.
- **Custom OG-image banner**: replace the `capsule-render` hero with a
  hand-designed SVG/PNG in `assets/` for full control over layout — trades
  automation for a fully bespoke look.

---

## 7. Performance notes

- All stat widgets are external, cached, edge-served images — they add
  network requests but no build cost to your profile page itself.
- Keep the README under roughly 500 lines of rendered content; GitHub does
  not hard-fail on longer profile READMEs, but very long pages hurt first
  impression and mobile scroll experience more than they help.
- Avoid stacking more than ~3 large `<img>`-based stat cards per row — on
  mobile these force horizontal scrolling if widths aren't set with `%`
  (this README always uses `width="%"`, not fixed `px`, for exactly that
  reason).
