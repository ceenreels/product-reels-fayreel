# Issue tracker: GitHub

Issues and specs for this repository live in:
https://github.com/ceenreels/product-reels-fayreel/issues

Use the `gh` CLI from this repository. Before the first issue write in a session,
check `gh repo view --json nameWithOwner`; the target must be
`ceenreels/product-reels-fayreel`. From another directory, pass
`--repo ceenreels/product-reels-fayreel` explicitly.

Record public documentation, the unified installer, releases, and parent-repo
integration work here. Record Admin, App, and Web implementation work in their
respective repositories, using `.gitmodules` and each component's agent
instructions to locate them. Link related issues for work across repositories.
Keep public issue bodies appropriate for this public repository.

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
