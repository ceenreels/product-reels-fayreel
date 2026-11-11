# Issue tracker: GitHub

Issues and specs for this repository live in:
https://github.com/ceenreels/product-reels-fayreel/issues

Use the `gh` CLI from this repository. Before the first issue write in a session,
check `gh repo view --json nameWithOwner`; the target must be
`ceenreels/product-reels-fayreel`. From another directory, pass
`--repo ceenreels/product-reels-fayreel` explicitly.

Record public documentation, the unified installer, releases, and parent-repo
integration work here. Record business research and planning in the private
`ceenreels/product-reels-fayreel-business` repository at `Business/`; record
Admin, App, and Web implementation in their respective repositories. Use
`.gitmodules` and each submodule's agent instructions to locate them.
Link related Issues for work across repositories. Public Issues and PRs contain
only integration metadata or explicitly authorized public summaries; keep
private research, plans, budgets, and results in their owning private repository.

## Issue before changes

Direct chat is a request intake channel. When the user's request calls for a
repository change, the agent must turn the discussion into an owning GitHub
Issue as part of that task, without waiting for the user to ask separately or
requiring the user to file it. This applies to bugs, features, optimizations,
and small edits, including code, tests, scripts, configuration, documentation,
agent instructions, and skills. Discussion and read-only investigation may
precede an Issue; creating an implementation branch or editing repository files
requires the following gate.

1. **Locate and reuse:** verify the owning repository and search its open and
   closed Issues. Read a matching open Issue and update it rather than duplicating
   the task. For a closed Issue, establish recurrence before reopening it or
   creating a distinct follow-up. Split cross-repository work into owning Issues
   and link them; keep public reports suitable for public disclosure.
2. **Write the agreed scope:** capture the problem or need, expected behavior,
   affected scope, constraints, and observable acceptance criteria. For a bug,
   include available reproduction steps and evidence. Separate facts from
   hypotheses and mark unknowns. The Issue must be understandable without this
   chat. If an implementation-critical detail is unresolved, record what is
   known, ask the focused question, and keep dependent changes pending.
3. **Publish and verify:** create or update the Issue, read it back to confirm
   the scope was saved, and report its URL in the conversation. A local draft,
   plan, or PR description does not satisfy this gate. If access or publication
   fails, preserve a draft outside the repository, explain the blocker, and
   continue only read-only work until the Issue is available.
4. **Branch, then edit:** only after the Issue is confirmed, fetch the default
   branch and create the task's temporary branch with its Issue number, then
   make changes. When resuming, verify and reuse the existing Issue and task
   branch. Preserve unrelated work and follow the delivery lifecycle below
   where defined; reference the Issue in commits and PRs.
5. **Keep the Issue current:** record later chat decisions and scope or acceptance
   changes before implementing them. Split a separate request into its own Issue
   when it does not belong to the existing task.

## Conventions

- Create: `gh issue create --title "..." --body-file <file>`.
- Read: `gh issue view <number> --json number,title,body,labels,comments`.
- List: `gh issue list --state open --json number,title,body,labels,comments`;
  add label and state filters as needed.
- Edit a body: `gh issue edit <number> --body-file <file>`.
- Comment: `gh issue comment <number> --body-file <file>`.
- Add or remove labels: `gh issue edit <number> --add-label "..."` or
  `--remove-label "..."`. Resolve triage roles through `triage-labels.md`.
- Close: post the explanation as a separate comment, then run
  `gh issue close <number>`. This preserves the explanation even when an issue
  was already closed.

For multiline bodies, write the exact text to a temporary file and use
`--body-file`, preserving newlines and literal characters.

## Parent issues and dependencies

- Create a child with `gh issue create --parent <parent> ...`, or attach an
  existing child with `gh issue edit <parent> --add-sub-issue <child>`.
- Record blockers with `gh issue edit <child> --add-blocked-by <blocker>`.
- Count open blockers with:
  `gh api repos/ceenreels/product-reels-fayreel/issues/<number> --jq .issue_dependencies_summary.blocked_by`.
- If native relationships are unavailable, use `Part of #<parent>` or
  `Blocked by: #<number>` at the top of the issue body.
- A ticket is unblocked when all its blockers are closed.

## Skill terminology

“Publish to the issue tracker” means create a GitHub issue.
“Fetch the relevant ticket” means read its body, labels, and comments.

## Pull requests as a triage surface

**PRs as a request surface: no.**

## Wayfinding operations

- Map: a single issue labelled `wayfinder:map`, with Notes, Decisions-so-far,
  and Fog sections in its body.
- Child ticket: an issue linked to the map as a sub-issue, labelled
  `wayfinder:<type>` (`research`, `prototype`, `grilling`, or `task`).
  If sub-issues are unavailable, use a task list in the map and a `Part of`
  reference in the child. Create a missing wayfinder label when first needed.
- Frontier: list the map's open children, drop those with an open blocker or
  assignee, and select the first remaining ticket in map order.
- Claim: `gh issue edit <number> --add-assignee @me` before working the ticket.
- Resolve: post the answer using `gh issue comment <number> --body-file <file>`,
  close the ticket, and append a brief finding plus its link to the map's
  Decisions-so-far section.
