# PROMPTS.md — my key prompts log

Keep the handful of prompts that actually moved the build. Not every message — the ones that
mattered: the system/sub-agent prompts, the ones you iterated on, the "this finally worked"
moment. This shows how you direct an AI, which is graded (challenge brief section 08).

Format per entry:
- **Prompt** (paste it)
- **For:** what you were trying to do
- **Revised?** did you have to change it, and why

---

## My Prompt

### Prompt 1

**Prompt:**
"Read rulebook.md and seo/detector.py..."

**For:**
Implementing remaining metadata and content detectors.

**Revised?**
No.

### Prompt 2
**Prompt:** The starter bundle's .claude/settings.json fails validation on Claude Code 2.1.167. Please inspect the current hook schema expected by this version and update .claude/settings.json so that the audit hooks continue writing to .claude/audit.jsonl.


**For:** Fixing audit logging.

**Revised?:** No. Claude identified missing type:"shell" fields.

### Prompt 3

**Prompt:**
Implement redirect_chain and redirect_loop detectors using a redirect graph built from Address -> Redirect URL mappings.

**For:**
Completing high-severity response code detection from the rulebook.

**Revised?**
No.
### Prompt 4

**Prompt:**
Review seo/detector.py and compare implemented detectors against rulebook.md. Identify which required detectors are still missing or not being triggered.

**For:**
Verification before continuing feature development.

**Revised?**
No.
### Prompt 5

**Prompt:**
Review seo/detector.py against rulebook.md line-by-line and identify missing or partially implemented detectors. Implement all missing detectors with strict deterministic Python logic and correct filtering rules.

**For:**
Completing full rulebook compliance for hidden export accuracy scoring.

**Revised?**
Yes — initially assumed full coverage existed, but verification showed rulebook gaps requiring additional detectors and stricter filtering.

### Prompt 6

**Prompt:**
Create a fix engine (seo/fixer.py) that generates SEO fixes including title rewrites, meta description rewrites, and redirect maps using deterministic selection + optional model-based text generation.

**For:**
Building champion-tier fix output for report.json and report.html.

**Revised?**
Yes — initially assumed fixes could be derived from detection layer, but separation required a dedicated fix pipeline.

### Prompt 7

**Prompt:**
Fix PermissionError WinError 10013 when starting ThreadingHTTPServer by adding automatic port fallback (7700+). Ensure SSE + MCP still works.

**For:**
Stabilizing dashboard startup on Windows systems where ports are sometimes locked.

**Revised?**
No.

---


