# Git Setup Log

## What was done

In `/Users/zz/zz/Documents/git-redo`, these steps were completed:

1. Initialized a local Git repository.
2. Added current project files.
3. Created the first commit (`83c6e01`, message: `Initial commit`).
4. Set the default branch to `main`.
5. Added GitHub remote:
   - `origin = https://github.com/ZackZhouHB/git-redo.git`
6. Pushed `main` to GitHub and set upstream tracking.

## Why these steps were needed

- The folder originally was not a Git repository (`fatal: not a git repository`).
- `git init` created local repository metadata (`.git/`).
- `git add` + `git commit` created the first snapshot to push.
- `git remote add origin ...` linked local repo to your GitHub repo.
- `git push -u origin main` published local history and connected local `main` to remote `origin/main`.

## How it is working now

Current verified state:

- Local repo exists (`.git` directory present).
- Branch tracking is active: `main...origin/main`.
- Remote is configured for both fetch and push:
  - `origin https://github.com/ZackZhouHB/git-redo.git`
- Latest commit is available locally and pushed:
  - `83c6e01 Initial commit`

This means new commits made in this folder can be pushed with `git push`, and remote updates can be pulled with `git pull`.
