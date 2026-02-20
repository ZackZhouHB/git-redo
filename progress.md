# Progress Tracker

## Purpose

This file is the continuity log for this repo.  
If the session disconnects or restarts, we can read this file and resume quickly.

## What You Are Trying To Do

- Learn and practice a real-world Git/GitHub workflow from `COURSE.md`.
- Use this repository as a hands-on training environment.
- Keep a persistent status record of work completed.

## Conversation + Work Log

### 2026-02-20

1. Verified Git access from CLI
- Ran `git status` in `/Users/zz/zz/Documents/git-redo`.
- Result: folder was not a Git repository yet.

2. Confirmed folder state
- Checked directory contents.
- Found only `COURSE.md` initially.

3. Initialized local Git and connected to GitHub
- Ran local setup (`git init`, first commit, branch to `main`, add `origin`).
- First push failed in sandbox due to network resolution.
- Retried push with elevated permissions.
- Result: `main` successfully pushed to `https://github.com/ZackZhouHB/git-redo.git`.

4. Verified repo health
- Confirmed:
  - tracking branch `main...origin/main`
  - remote fetch/push URLs are correct
  - latest commit was present

5. Added setup documentation
- Created `GIT_SETUP_LOG.md` describing what was done, why, and how it works.
- Committed and pushed:
  - commit `4acd346`
  - message `Add Git setup documentation`

6. Reviewed course content
- Read `COURSE.md` fully.
- Confirmed readiness to start training workflow.
- Detected `gh` CLI is not installed in this environment (`command not found`), so workflow uses Git CLI + GitHub web UI where needed.

7. Started Module 1 setup in repo
- Created:
  - `README.md`
  - `src/app.py`
  - `tests/test_app.py`
  - `docs/` directory
- Committed and pushed to `main`:
  - commit `62f3a4e`
  - message `chore: initial project setup`
- Created and pushed `develop` branch, with upstream tracking to `origin/develop`.

8. Saved continuity tracker and resumed work
- Committed and pushed this tracker file:
  - commit `0e1db2e`
  - message `docs: add session progress tracker`

9. Started and completed Module 2 implementation branch
- Created branch from `develop`:
  - `feature/PROJ-101-add-user-service`
- Added `src/user_service.py` and committed:
  - commit `f7520ce`
  - message `feat(PROJ-101): add UserService with create and get`
- Added `tests/test_user_service.py` and committed:
  - commit `e94cce8`
  - message `test(PROJ-101): add unit tests for UserService`
- Pushed feature branch to GitHub and set upstream tracking.

10. Confirmed GitHub branch protection and PR state
- User enabled branch protection on `main` in GitHub UI.
- Validated from CLI by attempting direct push to `main`; GitHub rejected with rule violation requiring PR.
- Verified open PR status with GitHub CLI:
  - PR `#1`
  - `feature/PROJ-101-add-user-service` -> `develop`
  - state `OPEN`
  - mergeable `CLEAN` / `MERGEABLE`
  - no reviews yet, no required checks configured.

## Current Status

- Local repo: initialized and healthy.
- Remote GitHub connection: working.
- `main`: pushed and tracking `origin/main`.
- `develop`: created, pushed, and tracking `origin/develop`.
- Module progress:
  - Module 1: complete (branch protection enabled and validated).
  - Module 2: complete (feature branch implemented, pushed, PR opened).

## Next Planned Step

- Continue to Module 3:
  - Add review comments on PR `#1` (simulate reviewer role).
  - Request changes.
  - Apply follow-up commit(s) on feature branch.
  - Re-request review and then approve/merge (squash).

## Ownership Clarity (Module 1)

- I did:
  - Local Git initialization and first commits.
  - Remote (`origin`) setup and push to GitHub.
  - Base project structure creation.
  - `develop` branch creation and push.
- You do:
  - Configure branch protection on `main` in GitHub UI:
    - Require pull request before merge
    - Require at least 1 approval
    - Require status checks / up-to-date branch (as desired for practice)

## Session State

- Status: Active.
- Resume point: Module 3 (PR + review simulation), while Module 1 branch protection may still be pending.
- Resume checklist:
  - Confirm branch protection is set on `main` in GitHub UI.
  - Open PR:
    - `feature/PROJ-101-add-user-service` -> `develop`
  - Continue Module 3 review cycle.

## Ownership Clarity (Current)

- I did:
  - Implemented Module 2 local coding workflow and pushed feature branch.
  - Verified branch protection enforcement and PR metadata from CLI.
- You do:
  - Complete GitHub UI actions:
    - (Module 3) perform review simulation in GitHub UI on PR `#1`

## Update Rule (for future turns)

After each completed job, append:
- date
- task requested
- actions taken
- outcome
- commit hash / branch / PR link (if applicable)
