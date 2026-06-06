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
"Validate missing-title detection using the exact rulebook filters rather than counting all blank title fields."

**For:**
Improving detector precision.

**Revised?:**
No.


---


