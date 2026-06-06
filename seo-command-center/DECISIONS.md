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
- `[14:58] Verified raw missing-title count was misleading because most rows were non-HTML or non-indexable. Confirmed rulebook filters must be applied before counting SEO issues.`


---

## My log
- `[--:--]` ...
