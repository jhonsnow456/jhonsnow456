# Setup & Customization Guide

This README is designed to live in a special repository: one whose name
**exactly matches your GitHub username** (e.g. `github.com/hey-amanthakur/hey-amanthakur`).
That's the only repo type GitHub renders as your profile page.

---

## 1. Folder structure

```
hey-amanthakur/                       ← repo name MUST equal your username
├── README.md                      ← the profile page itself
├── assets/
│   └── README.md
├── .github/
│   └── workflows/
│       └── snake.yml              ← contribution snake animation
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
| `GITHUB_TOKEN` | `snake.yml` | auto-provided by Actions | No setup needed; make sure the repo's Actions have **write** permission (Settings → Actions → General → Workflow permissions → Read and write). |

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
- **Snake animation**: if you fork/rename the repo, update the two
  `raw.githubusercontent.com/.../output/...` URLs in the README's
  "GitHub Analytics Room" section to match your new username/repo.

---

## 5. Graceful degradation

Every dynamic section is designed to fail safely:

- If a third-party stats service is down, the `<img>` tag simply renders as
  a broken image icon in that one card — it does not break the rest of the
  page. The public `github-readme-stats` instance is currently paused
  (returns 503), so this README now uses `github-profile-summary-cards`
  instead. For maximum reliability, self-host `github-readme-stats` on your
  own Vercel account (see below) and repoint the two `<img>` URLs at your
  instance.
- LeetCode/Codeforces/etc. are static link badges, not live widgets, by
  design — free third-party "stat card" services for these platforms are
  unreliable and rotate frequently. Swapping in a live one later is a
  drop-in change (replace the badge line with an `<img>` pointing at
  whichever service you choose).

---

## 6. Optional premium enhancements

- **Self-host github-readme-stats**: the shared public instance
  (`github-readme-stats.vercel.app`) is currently paused/503, which is why
  this README uses `github-profile-summary-cards` by default. For the exact
  original cards, fork `github-readme-stats`, deploy to Vercel with your own
  token, and point the two stat/language `<img>` URLs at your instance.
  Removes reliability risk from any shared public instance entirely.
- **WakaTime integration**: if you install the WakaTime CLI plugin in your
  editor, `github-readme-stats` can render a weekly coding-activity card
  automatically once your WakaTime API key is added as a secret
  (`WAKATIME_API_KEY`) — add:
  `![WakaTime](https://github-readme-stats.vercel.app/api/wakatime?username=hey-amanthakur)`
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
