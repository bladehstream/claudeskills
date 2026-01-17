---
argument-hint: [session-name]
description: Generate a context handoff document before running /clear. Optionally name the session for multi-session support.
---

# Context Handoff

**Session name (optional):** $ARGUMENTS

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

(Write "None" if the work is complete - don't invent future work)

## 5. LESSONS LEARNED
What was discovered during this session:
- **Constraints**: API quirks, environment issues, edge cases, performance considerations
- **Dead ends**: Approaches tried and abandoned (and WHY) - prevents fresh context from re-exploring
- **Bug patterns**: "If you see X error, the fix is Y"

## 6. CURRENT STATE
- Git status: committed/uncommitted changes, branch name
- Test status: what passes, what fails, what's untested
- Any running processes or background tasks

## 7. SESSION CONTEXT
Session-specific information that doesn't fit elsewhere:
- Debugging journey: sequence of problems encountered and how they were resolved
- Concurrent work: other sessions/branches that may interact with this work
- Warnings: procedural cautions (e.g., "don't commit file X - belongs to different session")

## 8. KEY COMMANDS
Quick-reference commands used in this work (copy-paste ready):
```
# Description of command
actual command here
```

## 9. PATHS DISCOVERED
Non-obvious file locations found during this session:
- Description: `/full/path/here`

## 10. VERIFICATION STEPS
How to confirm this work is correct:
1. Run `specific command`
2. Check URL/output for X
3. Expected result: Y

## 11. OPEN QUESTIONS
Unresolved decisions or ambiguities that need human input.
(These are blockers that cannot be resolved autonomously)

## 12. RESUMPTION PROMPT
Write the exact prompt to paste after /resume.

**Requirements:**
- Must be copy-paste ready with zero ambiguity
- Include full file paths, not relative
- Include branch name if relevant
- State the immediate next action
- Start with "Continue working on..."

---

**Output instructions:**
1. Create the `~/.claude/handoffs` directory if it doesn't exist
2. Determine the output file path:
   - If a session name was provided: `~/.claude/handoffs/handoff-{session-name}.md`
   - If no session name: `~/.claude/handoffs/handoff.md`
3. Write the complete handoff to the determined path
4. Confirm the file was written and remind the user:
   - If named session: run `/clear` followed by `/resume {session-name}` when ready to continue
   - If default session: run `/clear` followed by `/resume` when ready to continue
