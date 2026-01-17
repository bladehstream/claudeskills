---
argument-hint: [session-name]
description: Generate a context handoff document before running /clear. Optionally name the session for multi-session support.
---

# Context Handoff

**Session name (optional):** $1

I need to clear your context. Before I do, generate a comprehensive handoff document that will allow a fresh Claude instance to resume this work seamlessly.

**Determine the scenario that best fits our current state:**
- **MID_TASK**: Work is incomplete, context is degrading
- **TASK_COMPLETE**: Clean handoff to next phase of work
- **CHECKPOINT**: Saving state before a risky operation
- **SESSION_END**: Ending for now, will resume later

**Generate the following sections:**

## 1. OBJECTIVE
One paragraph stating what we are trying to achieve. Include the original user intent, not just the technical goal.

## 2. ARCHITECTURAL CONTEXT
- System/project structure relevant to this work
- Key files and their roles (with paths)
- Dependencies or integrations involved

## 3. WORK COMPLETED
Bulleted list of completed items with:
- What was done
- Key implementation decisions and WHY
- Any non-obvious approaches taken

## 4. WORK REMAINING
Bulleted list with:
- Task description
- Known blockers or dependencies
- Suggested approach (if known)

## 5. DISCOVERED CONSTRAINTS
Things learned during this session that aren't obvious from the code:
- API quirks, environment issues, edge cases
- Performance considerations
- Security or validation requirements discovered

## 6. REJECTED APPROACHES
What was tried and abandoned, and WHY. This prevents the fresh context from re-exploring dead ends.

## 7. CURRENT STATE
- Git status: committed/uncommitted changes
- Test status: what passes, what fails, what's untested
- Any running processes or background tasks

## 8. OPEN QUESTIONS
Unresolved decisions or ambiguities that need human input.

## 9. RESUMPTION PROMPT
Write the exact prompt to paste after /resume. Start with "Continue working on..." and include enough context that a fresh Claude instance can pick up immediately without asking clarifying questions.

---

**Output instructions:**
1. Create the `.claude/handoffs` directory if it doesn't exist
2. Determine the output file path:
   - If a session name was provided: `.claude/handoffs/handoff-{session-name}.md`
   - If no session name: `.claude/handoffs/handoff.md`
3. Write the complete handoff to the determined path
4. Confirm the file was written and remind the user:
   - If named session: run `/clear` followed by `/resume {session-name}` when ready to continue
   - If default session: run `/clear` followed by `/resume` when ready to continue
