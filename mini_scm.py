#!/usr/bin/env python3
"""
PySCM (Mini-SCM) - A Standalone Source Code Management / Version Control System
-------------------------------------------------------------------------------
Built from scratch in Python with zero external dependencies to demonstrate
how SCM systems (like Git) function under the hood:
- Content-addressable object store (SHA-1 hashing)
- Staging area / Index tracking
- Commit objects, parent references & Directed Acyclic Graph (DAG)
- Branch heads and HEAD pointer
- History logging and diff inspection

Usage:
  python mini_scm.py init
  python mini_scm.py add <file1> <file2> ... or python mini_scm.py add .
  python mini_scm.py commit -m "Commit message"
  python mini_scm.py status
  python mini_scm.py log
  python mini_scm.py branch [branch-name]
  python mini_scm.py checkout <branch-name>
  python mini_scm.py diff
"""

import os
import sys
import hashlib
import json
import time
from datetime import datetime

SCM_DIR = ".pyscm"
OBJECTS_DIR = os.path.join(SCM_DIR, "objects")
REFS_DIR = os.path.join(SCM_DIR, "refs", "heads")
HEAD_FILE = os.path.join(SCM_DIR, "HEAD")
INDEX_FILE = os.path.join(SCM_DIR, "index")

def hash_content(data: bytes) -> str:
    """Compute SHA-1 hash of raw byte contents (same hash algorithm as Git)."""
    return hashlib.sha1(data).hexdigest()

def write_object(data: bytes, obj_type: str = "blob") -> str:
    """Store object in .pyscm/objects/<hash[:2]>/<hash[2:]>."""
    header = f"{obj_type} {len(data)}\0".encode("utf-8")
    full_data = header + data
    obj_hash = hash_content(full_data)

    folder = os.path.join(OBJECTS_DIR, obj_hash[:2])
    os.makedirs(folder, exist_ok=True)
    obj_path = os.path.join(folder, obj_hash[2:])

    if not os.path.exists(obj_path):
        with open(obj_path, "wb") as f:
            f.write(full_data)

    return obj_hash

def read_object(obj_hash: str):
    """Read an object from the content-addressable store."""
    obj_path = os.path.join(OBJECTS_DIR, obj_hash[:2], obj_hash[2:])
    if not os.path.exists(obj_path):
        raise FileNotFoundError(f"Object {obj_hash} not found in SCM store")
    with open(obj_path, "rb") as f:
        raw = f.read()
    null_idx = raw.find(b"\0")
    header = raw[:null_idx].decode("utf-8")
    obj_type, _ = header.split(" ")
    content = raw[null_idx + 1:]
    return obj_type, content

def load_index():
    """Load the current staging area / index."""
    if not os.path.exists(INDEX_FILE):
        return {}
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_index(index: dict):
    """Persist the staging area / index to disk."""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

def get_head_branch():
    """Read active branch name from HEAD file."""
    if not os.path.exists(HEAD_FILE):
        return "main"
    with open(HEAD_FILE, "r", encoding="utf-8") as f:
        ref = f.read().strip()
    if ref.startswith("ref: refs/heads/"):
        return ref[len("ref: refs/heads/"):]
    return ref

def get_branch_commit(branch_name: str):
    """Get latest commit hash for a branch."""
    path = os.path.join(REFS_DIR, branch_name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def set_branch_commit(branch_name: str, commit_hash: str):
    """Update branch reference to point to commit hash."""
    path = os.path.join(REFS_DIR, branch_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(commit_hash)

# --- SCM COMMAND IMPLEMENTATIONS ---

def cmd_init():
    """Initialize a new PySCM repository."""
    if os.path.exists(SCM_DIR):
        print(f"Reinitialized existing PySCM repository in {os.path.abspath(SCM_DIR)}")
        return

    os.makedirs(OBJECTS_DIR, exist_ok=True)
    os.makedirs(REFS_DIR, exist_ok=True)

    with open(HEAD_FILE, "w", encoding="utf-8") as f:
        f.write("ref: refs/heads/main\n")

    save_index({})
    print(f"✓ Initialized empty PySCM repository in {os.path.abspath(SCM_DIR)}")
    print("  Default branch: main")

def cmd_add(files):
    """Stage files for commit."""
    if not os.path.exists(SCM_DIR):
        print("Fatal: Not a PySCM repository (run 'python mini_scm.py init' first).")
        return

    index = load_index()
    tracked = 0

    target_files = []
    if "." in files:
        for root, dirs, filenames in os.walk("."):
            if ".pyscm" in root or ".git" in root or "node_modules" in root:
                continue
            for fname in filenames:
                rel = os.path.normpath(os.path.join(root, fname))
                target_files.append(rel)
    else:
        target_files = files

    for file_path in target_files:
        if not os.path.isfile(file_path):
            continue
        with open(file_path, "rb") as f:
            content = f.read()
        blob_hash = write_object(content, "blob")
        index[os.path.normpath(file_path)] = {
            "hash": blob_hash,
            "size": len(content),
            "mtime": os.path.getmtime(file_path)
        }
        tracked += 1

    save_index(index)
    print(f"✓ Staged {tracked} file(s) into PySCM index.")

def cmd_commit(message: str, author: str = "Developer <dev@bookstore.io>"):
    """Create a commit object from staged index."""
    if not os.path.exists(SCM_DIR):
        print("Fatal: Not a PySCM repository.")
        return

    index = load_index()
    if not index:
        print("Nothing to commit (working tree clean, staging area empty).")
        return

    branch = get_head_branch()
    parent = get_branch_commit(branch)

    # Serialize tree
    tree_data = json.dumps(index, sort_keys=True).encode("utf-8")
    tree_hash = write_object(tree_data, "tree")

    commit_payload = {
        "tree": tree_hash,
        "parent": parent,
        "author": author,
        "timestamp": int(time.time()),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message
    }

    commit_data = json.dumps(commit_payload, indent=2).encode("utf-8")
    commit_hash = write_object(commit_data, "commit")

    set_branch_commit(branch, commit_hash)

    short_hash = commit_hash[:7]
    print(f"[{branch} {short_hash}] {message}")
    print(f" {len(index)} files tracked in tree {tree_hash[:7]}")

def cmd_status():
    """Display current working directory and staging status."""
    if not os.path.exists(SCM_DIR):
        print("Fatal: Not a PySCM repository.")
        return

    branch = get_head_branch()
    commit = get_branch_commit(branch)
    index = load_index()

    print(f"On branch: \033[92m{branch}\033[0m")
    if commit:
        print(f"Latest commit: \033[94m{commit[:7]}\033[0m")
    else:
        print("No commits yet on this branch.")

    print(f"\nStaged files ({len(index)}):")
    for fpath, meta in list(index.items())[:10]:
        print(f"  \033[92mnew file:   {fpath}\033[0m (blob {meta['hash'][:7]})")
    if len(index) > 10:
        print(f"  ... and {len(index) - 10} more files.")

def cmd_log():
    """Display commit log graph."""
    if not os.path.exists(SCM_DIR):
        print("Fatal: Not a PySCM repository.")
        return

    branch = get_head_branch()
    commit_hash = get_branch_commit(branch)

    if not commit_hash:
        print(f"No commits found on branch '{branch}'.")
        return

    print("=" * 60)
    print(f"PySCM Revision Log (Branch: {branch})")
    print("=" * 60)

    curr = commit_hash
    while curr:
        try:
            _, raw = read_object(curr)
            data = json.loads(raw.decode("utf-8"))
            print(f"\033[93mcommit {curr}\033[0m (HEAD -> \033[92m{branch}\033[0m)")
            print(f"Author: {data['author']}")
            print(f"Date:   {data.get('date', '')}")
            print(f"\n    {data['message']}\n")
            curr = data.get("parent")
        except Exception:
            break

def cmd_branch(name: str = None):
    """List or create branches."""
    if not os.path.exists(SCM_DIR):
        print("Fatal: Not a PySCM repository.")
        return

    active = get_head_branch()

    if not name:
        print("PySCM Branches:")
        for fname in os.listdir(REFS_DIR):
            prefix = "* " if fname == active else "  "
            color = "\033[92m" if fname == active else ""
            reset = "\033[0m" if fname == active else ""
            print(f"{prefix}{color}{fname}{reset}")
    else:
        # Create branch pointing to current commit
        curr_commit = get_branch_commit(active) or ""
        set_branch_commit(name, curr_commit)
        print(f"✓ Created branch '{name}' pointing to {curr_commit[:7] or 'initial'}")

def cmd_checkout(branch_name: str):
    """Switch to specified branch."""
    if not os.path.exists(SCM_DIR):
        print("Fatal: Not a PySCM repository.")
        return

    branch_file = os.path.join(REFS_DIR, branch_name)
    if not os.path.exists(branch_file):
        print(f"Error: Branch '{branch_name}' not found. Create it with 'python mini_scm.py branch {branch_name}'")
        return

    with open(HEAD_FILE, "w", encoding="utf-8") as f:
        f.write(f"ref: refs/heads/{branch_name}\n")
    print(f"✓ Switched to branch '{branch_name}'")

# CLI Entrypoint
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()

    if cmd == "init":
        cmd_init()
    elif cmd == "add":
        files = sys.argv[2:] if len(sys.argv) > 2 else ["."]
        cmd_add(files)
    elif cmd == "commit":
        msg = "Auto commit"
        if "-m" in sys.argv:
            idx = sys.argv.index("-m")
            if idx + 1 < len(sys.argv):
                msg = sys.argv[idx + 1]
        cmd_commit(msg)
    elif cmd == "status":
        cmd_status()
    elif cmd == "log":
        cmd_log()
    elif cmd == "branch":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_branch(name)
    elif cmd == "checkout":
        if len(sys.argv) < 3:
            print("Usage: python mini_scm.py checkout <branch-name>")
            return
        cmd_checkout(sys.argv[2])
    else:
        print(f"Unknown command: '{cmd}'. Run 'python mini_scm.py' for usage.")

if __name__ == "__main__":
    main()
