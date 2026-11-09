# Agent Instructions

Static company website for bengesoftwarellc.com (see [README.md](README.md)
for local preview and publishing details).

## MakeItOurs Ticket Tracking

For MakeItOurs work, keep related GitHub Issues and the private personal
[MakeItOurs Project #2](https://github.com/users/brandon-benge/projects/2)
current as part of the task. Routine updates to task-related issue context,
Project membership, and status are expected without a separate reminder.
This applies when starting here or entering `makeitours/`; read that
workspace's and the affected component's instructions before implementation.

- At task start, find the existing issues for the requested work in the
  owning repositories and read their acceptance criteria and latest evidence.
  Reuse those issues; do not create duplicate tickets or create a ticket just
  to populate the board. Do not add unrelated company/portfolio work to the
  MakeItOurs Project.
- Ensure every MakeItOurs issue created or worked on is on Project #2. Check
  membership first; add a missing existing issue with
  `gh project item-add 2 --owner brandon-benge --url <issue-url>`.
  Adding an issue to the Project does not create a new issue.
- Set **Todo** for unstarted work, **In Progress** once work begins (including
  partial implementation or pending required acceptance), and **Done** only
  when the issue's actual acceptance criteria are satisfied. A commit, merged
  PR, deployment, or passing unit suite alone does not prove live/device or
  release acceptance. Record blockers in the issue while leaving it open.
- Before finishing or handing off, update affected issues with a concise
  dated summary, evidence links, verification results, and specific remaining
  work. Reconcile Issue open/closed state and Project status; preserve criteria
  and concurrent edits. Do not silently narrow scope to declare completion.
  Keep private traces, credentials, designs, and account details out of public
  tickets. Avoid no-op comments and updates to unrelated tickets.
- Use `gh project field-list 2 --owner brandon-benge --format json` and
  `gh project item-list 2 --owner brandon-benge --limit 1000 --format json`
  to discover current field/item/option IDs, then `gh project item-edit` to
  update Status. Paginate if the Project exceeds the requested limit. Use an
  existing authorized GitHub account with repository and Project access;
  never print credentials or silently change global authentication settings.
- Re-read each changed issue and Project item to verify the saved state.
  Report ticket links and status changes in the final handoff. If access or
  permissions prevent an update, state exactly which update remains undone;
  do not claim tracking is current. Continue independent authorized work.

This is tracking authorization, not approval to commit, push, create/merge
PRs, deploy, change runtime settings, or run paid acceptance tests. The same
tracking rule is repeated in `makeitours/AGENTS.md` because it is a separate
Git root; keep both copies aligned when changing this policy.

## Contact Emails

Never use a personal email address (e.g. `llcbrandonbenge@gmail.com`)
anywhere in this website or the `makeitours/makeitours-website/` source
(published at `/makeitours-website/`). Always use one of
the following `@bengesoftwarellc.com` addresses, chosen by the purpose of the
page or section:

- `feature@bengesoftwarellc.com` — feature requests, roadmap suggestions.
- `privacy@bengesoftwarellc.com` — privacy policy questions, data requests.
- `makeitours-support@bengesoftwarellc.com` — MakeItOurs bug reports,
  problem reports, troubleshooting and product support (owner, 2026-11-09,
  makeitours#92).
- `support@bengesoftwarellc.com` — bug reports, troubleshooting, product
  support outside MakeItOurs.
- `contact@bengesoftwarellc.com` — general inquiries, terms questions,
  anything that doesn't fit the categories above.

If a new page needs a contact address, pick the closest match from this list
rather than introducing a new address or reusing a personal one.

## Git Persistence

Use plain Git to commit and push when explicitly requested. Do not use
autocommit or its wrappers. Creating or merging pull requests requires user
authorization; a commit-and-push request alone does not authorize deployment.
