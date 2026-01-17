---
description: Load a previously saved handoff document after /clear to resume work with full context.
---

# Resume from Handoff

Load and process the handoff document from a previous session.

**Instructions:**

1. Read the file `.claude/handoff.md`

2. If the file doesn't exist, inform the user:
   - "No handoff file found at `.claude/handoff.md`"
   - "Run `/handoff` before `/clear` to create one"
   - Ask if they want to describe what they were working on instead

3. If the file exists:
   - Parse and internalize all sections
   - Acknowledge the scenario (MID_TASK, TASK_COMPLETE, CHECKPOINT, or SESSION_END)
   - Summarize the objective and current state in 2-3 sentences
   - List the immediate next steps from WORK REMAINING
   - Note any OPEN QUESTIONS that need resolution
   - Execute the RESUMPTION PROMPT to continue work

4. After successfully loading, delete the handoff file to prevent stale reloads:
   - `rm .claude/handoff.md`

5. Begin work immediately based on the resumption prompt unless there are blocking open questions
