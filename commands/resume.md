---
argument-hint: [session-name] [--keep]
description: Resume from a handoff. Optionally specify session name. Use --keep to preserve the handoff file.
---

# Resume from Handoff

**Arguments provided:** $ARGUMENTS

Load and process the handoff document from a previous session.

**Instructions:**

1. Parse the arguments:
   - Extract session name (if any word not starting with `--`)
   - Check for `--keep` flag

2. Determine the handoff file path:
   - If a session name was provided: `.claude/handoffs/handoff-{session-name}.md`
   - If no session name: `.claude/handoffs/handoff.md`

3. Read the handoff file

4. If the file doesn't exist, inform the user:
   - "No handoff file found at `{path}`"
   - "Run `/handoff` or `/handoff {session-name}` before `/clear` to create one"
   - Ask if they want to describe what they were working on instead

5. If the file exists:
   - Parse and internalize all sections
   - Acknowledge the scenario (MID_TASK, TASK_COMPLETE, CHECKPOINT, or SESSION_END)
   - Summarize the objective and current state in 2-3 sentences
   - List the immediate next steps from WORK REMAINING
   - Note any OPEN QUESTIONS that need resolution

6. Handle file cleanup:
   - If `--keep` flag was provided: leave the handoff file in place
   - If `--keep` flag was NOT provided: delete the handoff file to prevent stale reloads

7. Execute the RESUMPTION PROMPT to continue work (unless there are blocking open questions)
