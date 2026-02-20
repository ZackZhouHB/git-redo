# Git Corporate Workflow — Hands-On Course

> Simulating real-world team git workflows using your own GitHub account.
> You'll play multiple roles: Developer A, Developer B, Tech Lead, and Reviewer.

---

## Prerequisites

- Your own GitHub account
- `gh` CLI installed (recommended): `brew install gh` then `gh auth login`
- Or use GitHub web UI for PR operations

---

## Module 1: Repository & Branch Strategy Setup

**What you'll learn:** How real orgs structure repos and branches.

### 1.1 Create the Repo

```bash
# Create a new repo on GitHub called "team-project-sim"
gh repo create team-project-sim --public --clone
cd team-project-sim
```

Or create it on github.com and clone it.

### 1.2 Set Up Branch Protection (This is KEY in real orgs)

Real companies NEVER let anyone push directly to `main`. Set this up:

1. Go to GitHub → your repo → Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (set to 1) — *you'll bypass this as admin for practice*
   - ✅ Require status checks to pass (we'll add CI later)
   - ✅ Require branches to be up to date before merging
   - ✅ Do not allow bypassing the above settings (toggle OFF for solo practice)
4. Save

> **Interview tip:** "We use branch protection rules on main. No direct pushes.
> All changes go through PRs with at least one approval and passing CI."

### 1.3 The Branching Strategy (Git Flow Lite / Trunk-Based)

Most big tech companies use one of these:

```
main          ← production code, always deployable
  └── develop ← integration branch (some teams skip this)
       ├── feature/JIRA-123-user-auth
       ├── feature/JIRA-456-payment-api
       ├── bugfix/JIRA-789-login-crash
       └── hotfix/JIRA-999-security-patch  ← branches off main directly
```

**Naming convention matters.** Real teams use:
- `feature/TICKET-ID-short-description`
- `bugfix/TICKET-ID-short-description`
- `hotfix/TICKET-ID-short-description`
- `release/v1.2.0`

```bash
# Set up initial project structure
echo "# Team Project Sim" > README.md
mkdir -p src tests docs
echo 'def hello(): return "Hello World"' > src/app.py
echo 'def test_hello(): assert hello() == "Hello World"' > tests/test_app.py
git add .
git commit -m "chore: initial project setup"
git push origin main

# Create develop branch
git checkout -b develop
git push origin develop
```

---

## Module 2: Feature Branch Workflow (The Daily Routine)

**What you'll learn:** How a developer picks up a ticket and delivers code.

### Scenario: You are Developer A, working on JIRA ticket PROJ-101

```bash
# STEP 1: Always start from the latest develop
git checkout develop
git pull origin develop

# STEP 2: Create feature branch with ticket ID
git checkout -b feature/PROJ-101-add-user-service

# STEP 3: Do your work in small, logical commits
cat > src/user_service.py << 'EOF'
class UserService:
    def __init__(self):
        self.users = {}

    def create_user(self, user_id, name):
        if user_id in self.users:
            raise ValueError("User already exists")
        self.users[user_id] = {"name": name}
        return self.users[user_id]

    def get_user(self, user_id):
        return self.users.get(user_id)
EOF

git add src/user_service.py
git commit -m "feat(PROJ-101): add UserService with create and get"

# STEP 4: Add tests (real teams require tests with features)
cat > tests/test_user_service.py << 'EOF'
from src.user_service import UserService

def test_create_user():
    svc = UserService()
    user = svc.create_user("u1", "Alice")
    assert user["name"] == "Alice"

def test_get_user_not_found():
    svc = UserService()
    assert svc.get_user("nope") is None
EOF

git add tests/test_user_service.py
git commit -m "test(PROJ-101): add unit tests for UserService"

# STEP 5: Push feature branch to remote
git push origin feature/PROJ-101-add-user-service
```

### Commit Message Convention (Conventional Commits)

Real teams enforce this. Interviewers notice if you know it:

```
<type>(<scope>): <short description>

Types: feat, fix, docs, style, refactor, test, chore, ci
Scope: ticket ID or module name

Examples:
feat(PROJ-101): add user registration endpoint
fix(PROJ-202): resolve null pointer in payment flow
docs: update API documentation for v2
ci: add GitHub Actions workflow for linting
```

---

## Module 3: Pull Requests & Code Review

**What you'll learn:** Creating PRs, writing good descriptions, review process.

### 3.1 Create a Pull Request

```bash
# Using gh CLI
gh pr create \
  --base develop \
  --title "feat(PROJ-101): Add UserService" \
  --body "## What
Adds UserService with create/get user functionality.

## Why
Needed for the user management epic (PROJ-100).

## How
- New UserService class in src/user_service.py
- Unit tests in tests/test_user_service.py

## Testing
- [x] Unit tests pass
- [ ] Integration tests (N/A for this PR)

## Ticket
Closes PROJ-101"
```

Or do it on GitHub web UI — the template above is what real PRs look like.

### 3.2 Simulate Code Review (Play the Reviewer Role)

Go to your PR on GitHub. Now pretend you're the reviewer:

1. **Go to "Files changed" tab**
2. **Leave inline comments** — click the `+` next to a line:
   - "Consider adding input validation for `name` parameter"
   - "Should we add a `delete_user` method?"
   - "Nit: let's use type hints here"
3. **Submit review** with "Request changes"

### 3.3 Address Review Comments (Back to Developer Role)

```bash
# Make changes based on review
cat > src/user_service.py << 'EOF'
from typing import Optional

class UserService:
    def __init__(self):
        self.users: dict = {}

    def create_user(self, user_id: str, name: str) -> dict:
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if user_id in self.users:
            raise ValueError("User already exists")
        self.users[user_id] = {"name": name.strip()}
        return self.users[user_id]

    def get_user(self, user_id: str) -> Optional[dict]:
        return self.users.get(user_id)

    def delete_user(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
EOF

git add src/user_service.py
git commit -m "feat(PROJ-101): add validation, type hints, delete_user per review"
git push origin feature/PROJ-101-add-user-service
```

4. **Go back to PR** → Reply to each comment explaining what you changed
5. **Re-request review**
6. **Reviewer approves** → "LGTM 🚀" (Looks Good To Me)
7. **Merge the PR** using "Squash and merge" (most common in real teams)

> **Interview tip:** "We use squash merges to keep main/develop history clean.
> Each PR becomes one commit on the target branch."

---

## Module 4: Merge Conflicts (The Inevitable)

**What you'll learn:** Handling conflicts like a pro.

### Scenario: Two developers edit the same file

```bash
# === Developer A's branch ===
git checkout develop
git pull origin develop
git checkout -b feature/PROJ-102-add-email-to-user

# Modify user_service.py — add email field
sed -i '' 's/{"name": name.strip()}/{"name": name.strip(), "email": None}/' src/user_service.py
git add . && git commit -m "feat(PROJ-102): add email field to user"
git push origin feature/PROJ-102-add-email-to-user

# === Developer B's branch (simulate by branching from same point) ===
git checkout develop
git checkout -b feature/PROJ-103-add-role-to-user

# Modify same file — add role field
sed -i '' 's/{"name": name.strip()}/{"name": name.strip(), "role": "member"}/' src/user_service.py
git add . && git commit -m "feat(PROJ-103): add role field to user"
git push origin feature/PROJ-103-add-role-to-user
```

Now merge PROJ-102 first (create PR, merge it). Then when you try to merge PROJ-103:

```bash
# Update PROJ-103 branch with latest develop (which now has PROJ-102)
git checkout feature/PROJ-103-add-role-to-user
git fetch origin
git merge origin/develop
# CONFLICT! This is where you resolve it.

# After resolving in your editor:
git add .
git commit -m "merge: resolve conflict with PROJ-102 email field"
git push origin feature/PROJ-103-add-role-to-user
```

> **Interview tip:** "I pull the latest target branch into my feature branch
> and resolve conflicts locally before the PR can be merged. I never force push
> to shared branches."

### Rebase vs Merge (Know the difference for interviews)

```bash
# MERGE approach (creates a merge commit — preserves history)
git checkout feature/my-branch
git merge develop

# REBASE approach (replays your commits on top — cleaner history)
git checkout feature/my-branch
git rebase develop
# If conflicts: fix them, then git rebase --continue

# WHEN TO USE WHAT:
# - Rebase: your own feature branch, before creating PR (clean history)
# - Merge: shared branches, never rebase shared branches
# - Squash merge: when merging PR into develop/main (most teams do this)
```

---

## Module 5: CI/CD with GitHub Actions

**What you'll learn:** How PRs trigger automated checks.

### 5.1 Add a CI Workflow

```bash
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  pull_request:
    branches: [develop, main]
  push:
    branches: [develop, main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pytest
      - run: pytest tests/ -v

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install flake8
      - run: flake8 src/ --max-line-length=120
EOF

git checkout develop
git checkout -b ci/add-github-actions
git add .github/
git commit -m "ci: add GitHub Actions workflow for tests and linting"
git push origin ci/add-github-actions
# Create PR and merge
```

Now every future PR will show ✅ or ❌ status checks.

> **Interview tip:** "Our CI runs on every PR — tests, linting, security scans.
> PRs can't be merged unless all checks pass."

---

## Module 6: Release Workflow

**What you'll learn:** How teams cut releases.

```bash
# Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Bump version, update changelog
echo "1.0.0" > VERSION
cat > CHANGELOG.md << 'EOF'
# Changelog

## v1.0.0 (2026-02-20)
- feat: Add UserService with CRUD operations (PROJ-101)
- feat: Add email field to user (PROJ-102)
- feat: Add role field to user (PROJ-103)
EOF

git add .
git commit -m "chore(release): prepare v1.0.0"
git push origin release/v1.0.0

# Create PR: release/v1.0.0 → main
# After merge, tag it:
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Back-merge main into develop
git checkout develop
git merge main
git push origin develop
```

---

## Module 7: Hotfix Workflow (Production Emergency)

**What you'll learn:** How to patch production without disrupting ongoing work.

```bash
# URGENT: Bug in production!
git checkout main
git pull origin main
git checkout -b hotfix/PROJ-999-fix-crash-on-empty-id

# Fix the bug
cat >> src/user_service.py << 'EOF'

    def create_user(self, user_id: str, name: str) -> dict:
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        # ... rest of method
EOF

# Actually just edit the file properly, then:
git add .
git commit -m "fix(PROJ-999): validate user_id is not empty"
git push origin hotfix/PROJ-999-fix-crash-on-empty-id

# Create PR → main (skip develop, this is urgent)
# After merge + deploy, back-merge to develop:
git checkout develop
git merge main
git push origin develop
```

> **Interview tip:** "Hotfixes branch off main, merge to main, then get
> back-merged to develop so the fix isn't lost."

---

## Module 8: Advanced Scenarios for Interviews

### 8.1 Git Stash (Context switching)
```bash
# You're mid-feature, but need to fix something urgent
git stash save "WIP: halfway through PROJ-200"
git checkout -b hotfix/urgent-thing
# ... fix, commit, push, PR ...
git checkout feature/PROJ-200-my-feature
git stash pop
```

### 8.2 Cherry-Pick (Bring specific commit to another branch)
```bash
# A fix on develop needs to go to main immediately
git log --oneline develop  # find the commit hash
git checkout main
git cherry-pick <commit-hash>
git push origin main
```

### 8.3 Interactive Rebase (Clean up before PR)
```bash
# You made 5 messy commits, clean them up before review
git rebase -i HEAD~5
# Mark commits as: pick, squash, fixup, reword
# This gives reviewers a clean, logical commit history
```

### 8.4 Git Bisect (Find which commit broke something)
```bash
git bisect start
git bisect bad          # current commit is broken
git bisect good v1.0.0  # this version worked
# Git checks out middle commit, you test, mark good/bad
# Repeat until it finds the exact breaking commit
git bisect reset
```

### 8.5 CODEOWNERS File (Auto-assign reviewers)
```bash
cat > .github/CODEOWNERS << 'EOF'
# These owners are auto-requested for review
src/user_service.py    @backend-team
src/payment/           @payments-team
*.yml                  @devops-team
docs/                  @tech-writers
EOF
```

---

## Module 9: Interview Cheat Sheet

### "Describe your team's git workflow"

> "We follow a trunk-based development approach with short-lived feature branches.
> Developers branch off develop with a naming convention like feature/TICKET-ID-description.
> We make small, focused commits using conventional commit messages.
> When ready, we open a PR against develop. CI runs automatically — tests, linting,
> security scans. We need at least one approval from a code owner. We use squash merge
> to keep history clean. For releases, we cut a release branch, merge to main, tag it,
> and back-merge. Hotfixes go directly off main for emergencies."

### "How do you handle merge conflicts?"

> "I fetch the latest target branch and merge it into my feature branch locally.
> I resolve conflicts in my editor, run tests to make sure nothing broke,
> then push. I never force push to shared branches. If the conflict is complex,
> I'll pull in the other developer to resolve it together."

### "How do you do code reviews?"

> "I look at the PR description first to understand the context. Then I review
> the diff file by file. I check for correctness, edge cases, naming, test coverage,
> and potential performance issues. I leave inline comments and categorize them —
> blockers vs nits. I approve only when I'm confident the code is production-ready."

### Common terms to know:
- **PR/MR** — Pull Request (GitHub) / Merge Request (GitLab)
- **LGTM** — Looks Good To Me
- **CODEOWNERS** — auto-assigns reviewers based on file paths
- **Branch protection** — rules preventing direct pushes to main
- **Squash merge** — combine all PR commits into one
- **Rebase** — replay commits on top of another branch
- **Cherry-pick** — copy a specific commit to another branch
- **Git bisect** — binary search for the commit that introduced a bug
- **Trunk-based development** — short-lived branches, frequent merges
- **Git flow** — more structured with develop/release/hotfix branches
- **Feature flags** — deploy code without enabling it (decouple deploy from release)

---

## Practice Order

1. ✅ Module 1 — Set up repo + branch protection
2. ✅ Module 2 — Feature branch workflow
3. ✅ Module 3 — Create PR + simulate review
4. ✅ Module 5 — Add CI (so future PRs have checks)
5. ✅ Module 4 — Create a merge conflict and resolve it
6. ✅ Module 6 — Cut a release
7. ✅ Module 7 — Simulate a hotfix
8. ✅ Module 8 — Practice advanced scenarios
9. ✅ Module 9 — Rehearse interview answers out loud

**Time estimate:** 3-4 hours for the full course, or 1 hour if you focus on Modules 2-4 + 9.
