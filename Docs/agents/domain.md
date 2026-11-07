# Domain docs

## Layout and scope

Use single-context domain documentation for this public parent repository:

- `GLOSSARY.md` at the repository root for agreed terminology.
- `Docs/adr/` for architecture and workflow decisions.

Paths are relative to this repository root and preserve the existing `Docs/`
capitalization. Component repositories under `Src/` maintain their own domain
docs and agent instructions; read those when working inside a component.

## Before exploring

Read `GLOSSARY.md` and ADRs relevant to the work. If `GLOSSARY-MAP.md` is adopted
later, follow its pointers to the relevant context glossaries.

If these files or directories do not exist, proceed silently. Create them
lazily through `domain-modeling` when terms or decisions are actually resolved;
setup does not require empty placeholders.

## Use the glossary's vocabulary

Use agreed terms in issue titles, proposals, hypotheses, code, and tests. If a
needed term is missing, reconsider the wording or note the gap for
`domain-modeling`.

## Flag ADR conflicts

When a proposal conflicts with an existing ADR, identify the ADR and explain
why the decision should be revisited rather than silently overriding it.
