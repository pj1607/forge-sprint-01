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


---

## My log
- `[--:--]` ...
