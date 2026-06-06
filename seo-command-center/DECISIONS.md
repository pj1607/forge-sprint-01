# DECISIONS.md — decision & learnings log

A short running note of the real choices you made: what you tried, what failed and why, what
you changed. This is your engineering judgement on the record — it is what separates a builder
from a button-presser, and it is graded (challenge brief section 08).

Append a 1–2 line entry whenever you make a real decision or hit/fix a wall. Add a timestamp.

Format:
`[HH:MM] <decision or problem> → <what you did and why>`

---

- `[14:15] Prioritized detector implementation before AI-generated fixes → issue detection accuracy is worth more leaderboard points than title rewriting.`
- `[14:25] Claude Code 2.1.167 rejected starter hook schema → added type:"shell" to all hook definitions and verified audit.jsonl logging with manual test.`
- `[14:33] Performed detector verification before adding new features → wanted to confirm issue counts and rulebook compliance before extending the audit engine.`
- `[14:49] Prioritized redirect graph analysis before report generation → redirect chains and loops are High severity and directly affect detection accuracy.`
- `[15:06] Detector output remained at 12 issue types after adding redirect analysis → paused feature work and verified detector implementation before proceeding.`
- `[15:20] Model claimed 100% detector coverage → rejected claim and enforced rulebook line-by-line verification for accuracy.`
- `[15:24] Decided to enforce strict filter rule (HTML + indexable + 200) globally → prevents false positives in meta/title detectors.`
- `[15:28] Prioritized deterministic completeness over ML fixes → scoring depends on exact rule compliance, not heuristic outputs.`
- `[15:45] Separated fix logic from detection logic → improves architecture clarity and scoring alignment.`
- `[15:46] Restricted model usage to text rewriting only → prevents nondeterministic scoring errors.`
- `[15:47] Introduced deterministic redirect mapping strategy → ensures reproducibility on hidden export.`
- `[15:55] Dashboard crash due to WinError 10013 → decided to implement dynamic port fallback (7700+ increment) instead of forcing manual port kill to improve usability and judge reliability score.`

- `[15:58] Chose stability over fixed port assumption → system now self-heals port conflicts and prints active URL.`


---

## My log
- `[--:--]` ...
