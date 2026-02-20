# Git + PR Workflow Concepts (Beginner Notes)

## Why This File Exists

This is a simple reference for core Git/PR concepts and real-world team practices.  
It captures the basic questions asked during the course so they are easy to review later.

## Core Branch Roles

- `main`:
  - Production branch.
  - Protected.
  - Usually only updated via pull requests.
- `develop`:
  - Integration branch (used in Git-flow-lite teams).
  - Multiple finished feature branches merge here first.
  - Later promoted to `main` during release.
- `feature/*`:
  - Short-lived branch for one ticket/task.
  - Created from `develop` (or `main` in trunk-based teams).
  - Merged back by PR.

## Typical PR Sequence

1. Developer pulls latest target branch locally.
2. Developer creates local feature branch.
3. Developer makes changes and commits locally.
4. Developer pushes feature branch to remote.
5. Developer opens PR to target branch.
6. Reviewer leaves comments or requests changes.
7. Developer pushes follow-up commits to same feature branch.
8. PR updates automatically.
9. Reviewer approves and PR is merged (often squash merge).

## Important Clarifications

- PR is usually created after the feature branch is pushed.
- A PR can stay open while the developer keeps pushing new commits.
- In solo practice, one person can simulate both reviewer and developer roles.
- On GitHub, PR author cannot always do a true blocking self-review; comments still help simulate workflow.

## Who Approves in Real Companies

- Not one person for everything.
- Approval is usually by code owners of changed files/areas.
- `CODEOWNERS` auto-requests reviewers by path ownership.
- Branch protection enforces approval + checks before merge.

## `Conversation` / `Commits` / `Checks` / `Files changed`

- `Conversation`:
  - Context, decisions, risk, rollout notes.
- `Commits`:
  - Commit history and follow-up changes.
- `Checks`:
  - CI results (tests, lint, security, build).
- `Files changed`:
  - Line-by-line correctness review.

## CI vs CI/CD and PR Behavior

- `CI` (Continuous Integration):
  - Automatically runs validation (test/lint/build) on pushes/PRs.
- `CD` (Continuous Delivery/Deployment):
  - Delivers or deploys after CI passes (often with policy gates).
- `CI/CD`:
  - Refers to both together.

Practical PR behavior:
- Opening or updating a PR triggers configured CI workflows.
- If a check fails, the PR is not auto-closed; it stays open.
- Branch protection can block merge until required checks pass.
- Developer pushes a fix to the same branch; checks rerun automatically.

Industry-standard detail:
- In PR-based workflows, new commits pushed to an already-open PR branch trigger CI again on that same PR.
- This is normal expected behavior across major CI platforms (GitHub Actions, GitLab CI, CircleCI, Jenkins PR jobs, Buildkite).

## Trunk-Based vs Develop-Based

- Trunk-based:
  - One main trunk branch.
  - Short-lived feature branches.
  - Frequent merge to trunk.
- Develop-based (this course):
  - Features merge into `develop`.
  - Release step moves `develop` to `main`.

Both are used in industry. Large companies often prefer trunk-based with strong CI and feature flags.

## Release Timing (`develop` -> `main`)

- Happens when a release is ready.
- Common release flow:
  - stabilize on `develop`
  - PR/merge to `main`
  - tag release
  - back-merge `main` to `develop` if needed

## Best Practices to Remember

- Keep branches short-lived.
- Keep PRs small and focused.
- Use clear commit messages.
- Always include tests for new behavior.
- Reply to each review comment with what changed.
- Avoid direct pushes to protected branches.
- Prefer squash merge for clean history (if team policy uses it).
- Treat CI failures as useful feedback from a clean environment, not as a personal error.

## Your Practical Learning Milestones So Far

- Local repo initialized and linked to GitHub.
- Branch protection on `main` validated.
- Feature PR created, updated after review-style feedback, and merged to `develop`.
- GitHub CLI access verified for PR inspection.
