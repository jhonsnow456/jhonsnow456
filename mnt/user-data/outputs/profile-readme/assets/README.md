# assets/

This folder holds generated, non-markdown data used by the README:

- `rpg-stats.json` — written by `scripts/compute_rpg_stats.py` on each
  scheduled run of `update-readme.yml`. Contains raw stats, computed XP/level,
  and achievement flags.
- Add any static images here (e.g. `banner.png`, project screenshots) and
  reference them from `README.md` with relative paths like
  `assets/banner.png` — this keeps the repo self-contained and avoids
  hot-linking issues.

Nothing in this folder needs to be edited by hand once the workflows are
configured; it exists so generated data has somewhere to live between runs.
