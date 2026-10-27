"""
NAAN MUDHALVAN - NM1130 AI AND DIGITAL SKILLS
EX.NO: 6  |  GitHub Foundations
------------------------------------------------------------------
Department  : CSE (AI & ML)
College     : University College of Engineering (BIT Campus), Anna University, Tiruchirappalli

Aim
---
To understand version control by building a tiny Git-like system in Python.
It demonstrates every key idea from the notes:

    repository, commit, branch, merge, clone, push, pull request, review

The simulator runs entirely in memory, so it is safe to run anywhere.
The real Git commands that match each step are printed alongside.

Libraries : standard library only
Run       : python mini_git.py
"""

import copy
import difflib
import hashlib
import time
from dataclasses import dataclass, field


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


@dataclass
class Commit:
    id: str
    message: str
    author: str
    parents: list
    snapshot: dict          # {filename: file content} at the time of the commit


@dataclass
class PullRequest:
    number: int
    title: str
    source: str
    target: str
    approvals: list = field(default_factory=list)
    state: str = "open"


class MiniGit:
    def __init__(self, name: str):
        self.name = name
        self.commits: dict[str, Commit] = {}
        self.branches: dict[str, str | None] = {"main": None}   # branch name -> latest commit id
        self.current = "main"
        self.working: dict[str, str] = {}   # files on your computer (working directory)
        self.index: dict[str, str] = {}     # staging area (files marked for the next commit)
        self.pull_requests: list[PullRequest] = []
        self.order: list[str] = []          # commit ids in the order they were created
        print(f"[git init] Created empty repository '{name}'")

    # ----- helpers ---------------------------------------------------------
    @property
    def head(self) -> str | None:
        return self.branches[self.current]

    def _head_snapshot(self) -> dict:
        return dict(self.commits[self.head].snapshot) if self.head else {}

    def _ancestors(self, commit_id: str | None) -> dict[str, int]:
        """All ancestors of a commit with their distance (used to find the merge base)."""
        seen, queue = {}, [(commit_id, 0)]
        while queue:
            cid, depth = queue.pop(0)
            if cid is None or cid in seen:
                continue
            seen[cid] = depth
            queue.extend((p, depth + 1) for p in self.commits[cid].parents)
        return seen

    # ----- everyday commands -------------------------------------------------
    def write(self, filename: str, content: str) -> None:
        self.working[filename] = content

    def add(self, *filenames: str) -> None:
        for name in filenames or self.working:
            self.index[name] = self.working[name]
        print(f"[git add] staged: {', '.join(filenames) if filenames else 'all changes'}")

    def status(self) -> None:
        base = self._head_snapshot()
        staged = [f for f in self.index if base.get(f) != self.index[f]]
        unstaged = [f for f in self.working if self.index.get(f) != self.working[f]]
        print(f"[git status] on branch '{self.current}' | staged: {staged or 'none'} | not staged: {unstaged or 'none'}")

    def commit(self, message: str, author: str = "student") -> str:
        if self.index == self._head_snapshot():
            print("[git commit] nothing to commit")
            return ""
        raw = f"{message}{self.head}{time.time_ns()}{sorted(self.index.items())}"
        cid = hashlib.sha1(raw.encode()).hexdigest()[:7]
        self.commits[cid] = Commit(cid, message, author, [self.head] if self.head else [], dict(self.index))
        self.branches[self.current] = cid
        self.order.append(cid)
        print(f"[git commit] [{self.current} {cid}] {message}")
        return cid

    def branch(self, name: str) -> None:
        self.branches[name] = self.head
        print(f"[git branch] created branch '{name}'")

    def checkout(self, name: str) -> None:
        if self.working != self.index or self.index != self._head_snapshot():
            raise RuntimeError("You have uncommitted changes - commit them before switching branches.")
        self.current = name
        self.working = self._head_snapshot()
        self.index = dict(self.working)
        print(f"[git checkout] switched to branch '{name}'")

    # ----- merging -----------------------------------------------------------
    def merge(self, other: str) -> None:
        ours, theirs = self.head, self.branches[other]
        if theirs in self._ancestors(ours):
            print("[git merge] already up to date")
            return
        if ours is None or ours in self._ancestors(theirs):           # fast-forward
            self.branches[self.current] = theirs
            self.working, self.index = dict(self.commits[theirs].snapshot), dict(self.commits[theirs].snapshot)
            print(f"[git merge] fast-forward '{self.current}' to {theirs}")
            return

        # three-way merge: find the common ancestor (merge base)
        theirs_anc = self._ancestors(theirs)
        base_id = min((c for c in self._ancestors(ours) if c in theirs_anc), key=lambda c: self._ancestors(ours)[c])
        base, a, b = self.commits[base_id].snapshot, self._head_snapshot(), self.commits[theirs].snapshot

        merged, conflicts = {}, []
        for f in sorted(set(base) | set(a) | set(b)):
            va, vb, v0 = a.get(f), b.get(f), base.get(f)
            if va == vb:
                value = va
            elif va == v0:
                value = vb                  # only the other branch changed it
            elif vb == v0:
                value = va                  # only we changed it
            else:
                conflicts.append(f)         # both changed the same file differently
                continue
            if value is not None:
                merged[f] = value

        if conflicts:
            print(f"[git merge] CONFLICT in {conflicts} - automatic merge failed, fix manually and commit")
            return
        self.working, self.index = dict(merged), dict(merged)
        cid = hashlib.sha1(f"merge{ours}{theirs}".encode()).hexdigest()[:7]
        self.commits[cid] = Commit(cid, f"Merge branch '{other}' into {self.current}", "student", [ours, theirs], merged)
        self.branches[self.current] = cid
        self.order.append(cid)
        print(f"[git merge] merged '{other}' into '{self.current}' -> {cid}")

    # ----- history -----------------------------------------------------------
    def log(self) -> None:
        print(f"[git log] branch '{self.current}':")
        history = self._ancestors(self.head)
        for cid in sorted(history, key=self.order.index, reverse=True):   # newest first
            c = self.commits[cid]
            marker = "merge" if len(c.parents) > 1 else "     "
            print(f"   * {cid} {marker} {c.message}  ({c.author})")

    def diff(self, old_id: str, new_id: str) -> None:
        print(f"[git diff] {old_id}..{new_id}")
        old, new = self.commits[old_id].snapshot, self.commits[new_id].snapshot
        for f in sorted(set(old) | set(new)):
            lines = difflib.unified_diff(old.get(f, "").splitlines(), new.get(f, "").splitlines(),
                                         f"a/{f}", f"b/{f}", lineterm="", n=0)
            for line in lines:
                print("   ", line)

    # ----- collaboration -----------------------------------------------------
    def clone(self, new_name: str) -> "MiniGit":
        twin = copy.deepcopy(self)
        twin.name = new_name
        print(f"[git clone] copied '{self.name}' to '{new_name}' ({len(self.commits)} commits)")
        return twin

    def open_pull_request(self, title: str, source: str, target: str = "main") -> PullRequest:
        pr = PullRequest(len(self.pull_requests) + 1, title, source, target)
        self.pull_requests.append(pr)
        print(f"[pull request #{pr.number}] opened: '{title}' ({source} -> {target})")
        return pr

    def review(self, pr: PullRequest, reviewer: str) -> None:
        pr.approvals.append(reviewer)
        print(f"[pull request #{pr.number}] approved by {reviewer}")

    def merge_pull_request(self, pr: PullRequest) -> None:
        if not pr.approvals:
            print(f"[pull request #{pr.number}] cannot merge - needs at least 1 approval")
            return
        saved = self.current
        self.checkout(pr.target)
        self.merge(pr.source)
        pr.state = "merged"
        print(f"[pull request #{pr.number}] merged (was on '{saved}')")


def main() -> None:
    print("NM1130 - EX.NO: 6 - GITHUB FOUNDATIONS (mini Git simulator)")

    heading("1. CREATE A REPOSITORY AND MAKE THE FIRST COMMIT   (git init / add / commit)")
    repo = MiniGit("student-project")
    repo.write("README.md", "# Student Project\nA small Python project.")
    repo.write("app.py", "print('Hello World')")
    repo.status()
    repo.add()
    repo.status()
    first = repo.commit("Initial commit: add README and app")

    heading("2. BRANCHING - work on a feature without touching main   (git branch / checkout)")
    repo.branch("feature-login")
    repo.checkout("feature-login")
    repo.write("login.py", "def login(user, pwd):\n    return user == 'admin'")
    repo.add()
    repo.commit("Add login module")
    repo.write("login.py", "def login(user, pwd):\n    return user == 'admin' and pwd == 'secret'")
    repo.add()
    second = repo.commit("Check password in login")
    repo.diff(first, second)

    heading("3. PARALLEL WORK ON MAIN, THEN MERGE   (git merge)")
    repo.checkout("main")
    repo.write("README.md", "# Student Project\nA small Python project.\n\n## Usage\nRun: python app.py")
    repo.add()
    repo.commit("Document usage in README")
    repo.merge("feature-login")
    repo.log()

    heading("4. MERGE CONFLICT - the same line edited in two branches")
    repo.branch("fix-greeting")
    repo.checkout("fix-greeting")
    repo.write("app.py", "print('Hello, Anna University!')")
    repo.add(); repo.commit("Change greeting")
    repo.checkout("main")
    repo.write("app.py", "print('Welcome to NM1130')")
    repo.add(); repo.commit("Change welcome text")
    repo.merge("fix-greeting")

    heading("5. COLLABORATION: CLONE -> BRANCH -> PULL REQUEST -> REVIEW -> MERGE")
    teammate = repo.clone("teammate-copy")
    teammate.branch("add-tests")
    teammate.checkout("add-tests")
    teammate.write("test_login.py", "from login import login\nassert login('admin', 'secret')")
    teammate.add()
    teammate.commit("Add unit test for login", author="teammate")
    # 'git push' - the teammate's branch reaches the shared GitHub repository
    repo.commits.update(teammate.commits)
    repo.order.extend(c for c in teammate.order if c not in repo.order)
    repo.branches["add-tests"] = teammate.branches["add-tests"]
    print("[git push] teammate's branch 'add-tests' uploaded to GitHub")

    pr = repo.open_pull_request("Add unit test for login", source="add-tests")
    repo.merge_pull_request(pr)          # fails: nobody has reviewed it yet
    repo.review(pr, "professor")
    repo.merge_pull_request(pr)
    repo.log()

    print("\nResult: Version-control workflow (commit, branch, merge, pull request) demonstrated.")


if __name__ == "__main__":
    main()
