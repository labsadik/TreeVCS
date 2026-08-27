import os
import sys
import json
import hashlib
import fnmatch
from datetime import datetime

__VERSION__ = "1.0.0"
__AUTHOR__ = "Sadik Laskar"
__APP_NAME__ = "Tree"

DEFAULT_IGNORES = [
    ".git",
    ".tree",
    "__pycache__",
    "*.pyc",
    "tree_installer*.exe",
    "dist",
    "build",
    "releases",
    "*.spec"
]

def load_ignore_patterns(root_dir):
    patterns = list(DEFAULT_IGNORES)
    ignore_file = os.path.join(root_dir, ".treeignore")
    if os.path.isfile(ignore_file):
        with open(ignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns

def is_ignored(name, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(name + "/", pattern):
            return True
    return False

def hash_file_content(filepath):
    sha = hashlib.sha1()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha.update(chunk)
        return sha.hexdigest()
    except Exception:
        return None

def get_tracked_files(root_dir, patterns):
    file_map = {}
    for current_root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not is_ignored(d, patterns)]
        for file in files:
            if not is_ignored(file, patterns):
                full_path = os.path.join(current_root, file)
                rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
                file_map[rel_path] = full_path
    return file_map

def sync_git_ui(action, targets=None, message=""):
    """Silently bridges to git so VS Code shows U and M badges."""
    if not os.path.exists(".git"):
        os.system("git init >nul 2>&1")
    
    if action == "add" and targets:
        target_str = " ".join(targets)
        os.system(f"git add {target_str} >nul 2>&1")
    elif action == "commit":
        os.system(f'git commit -m "{message}" >nul 2>&1')

def get_all_file_statuses(root_dir="."):
    if not os.path.exists(".tree"):
        return {}

    patterns = load_ignore_patterns(root_dir)
    working_files = get_tracked_files(root_dir, patterns)
    
    index = {}
    if os.path.exists(".tree/index.json"):
        with open(".tree/index.json", "r", encoding="utf-8") as f:
            index = json.load(f)

    head_commit_tree = {}
    if os.path.exists(".tree/HEAD.json"):
        with open(".tree/HEAD.json", "r", encoding="utf-8") as f:
            head = json.load(f)
        current_commit_hash = head["branches"].get(head["current_branch"])
        if current_commit_hash:
            commit_file = os.path.join(".tree/objects", current_commit_hash)
            if os.path.exists(commit_file):
                with open(commit_file, "r", encoding="utf-8") as f:
                    head_commit_tree = json.load(f).get("tree", {})

    status_map = {}
    for rel_path, full_path in working_files.items():
        curr_hash = hash_file_content(full_path)
        
        if rel_path in index:
            if rel_path not in head_commit_tree:
                status_map[rel_path] = "[staged]"
            elif index[rel_path] != head_commit_tree[rel_path]:
                status_map[rel_path] = "[staged]"
            elif curr_hash != index[rel_path]:
                status_map[rel_path] = "[modified]"
            else:
                status_map[rel_path] = "[clean]"
        else:
            if rel_path in head_commit_tree:
                if curr_hash != head_commit_tree[rel_path]:
                    status_map[rel_path] = "[modified]"
                else:
                    status_map[rel_path] = "[clean]"
            else:
                status_map[rel_path] = "[untracked]"

    return status_map

def init_repo():
    if os.path.exists(".tree"):
        print("Reinitialized existing Tree repository.")
    else:
        os.makedirs(".tree/objects", exist_ok=True)
        head_config = {"current_branch": "main", "branches": {"main": None}}
        with open(".tree/HEAD.json", "w", encoding="utf-8") as f:
            json.dump(head_config, f, indent=2)
        with open(".tree/index.json", "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

    if not os.path.exists(".treeignore"):
        with open(".treeignore", "w", encoding="utf-8") as f:
            f.write("# 🌳 Tree Ignore File\nnode_modules/\n*.log\nbuild/\ndist/\nreleases/\n")

    sync_git_ui("init")
    print("Initialized empty Tree repository in .tree/")

def add_files(targets):
    if not os.path.exists(".tree"):
        print("Fatal: Not a Tree repository (run 'tree init' first).")
        return

    patterns = load_ignore_patterns(".")
    with open(".tree/index.json", "r", encoding="utf-8") as f:
        index = json.load(f)

    all_files = get_tracked_files(".", patterns)
    files_to_stage = []

    for target in targets:
        if target == ".":
            files_to_stage.extend(all_files.keys())
        else:
            clean_target = target.replace("\\", "/")
            if clean_target in all_files:
                files_to_stage.append(clean_target)

    for rel_path in set(files_to_stage):
        full_path = all_files[rel_path]
        file_hash = hash_file_content(full_path)
        if file_hash:
            obj_path = os.path.join(".tree/objects", file_hash)
            with open(full_path, "rb") as src, open(obj_path, "wb") as dst:
                dst.write(src.read())
            index[rel_path] = file_hash
            print(f"Staged: {rel_path}")

    with open(".tree/index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    sync_git_ui("add", targets)

def commit_changes(message):
    if not os.path.exists(".tree"):
        print("Fatal: Not a Tree repository.")
        return

    with open(".tree/index.json", "r", encoding="utf-8") as f:
        index = json.load(f)

    if not index:
        print("Nothing to commit (stage files with 'tree add' first).")
        return

    with open(".tree/HEAD.json", "r", encoding="utf-8") as f:
        head = json.load(f)

    current_branch = head["current_branch"]
    parent_commit = head["branches"].get(current_branch)

    commit_data = {
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "parent": parent_commit,
        "tree": index
    }

    commit_json = json.dumps(commit_data, sort_keys=True).encode("utf-8")
    commit_hash = hashlib.sha1(commit_json).hexdigest()

    with open(os.path.join(".tree/objects", commit_hash), "w", encoding="utf-8") as f:
        f.write(json.dumps(commit_data, indent=2))

    head["branches"][current_branch] = commit_hash
    with open(".tree/HEAD.json", "w", encoding="utf-8") as f:
        json.dump(head, f, indent=2)

    sync_git_ui("commit", message=message)
    print(f"[{current_branch} {commit_hash[:7]}] {message}")

def show_log():
    if not os.path.exists(".tree"):
        print("Fatal: Not a Tree repository.")
        return

    with open(".tree/HEAD.json", "r", encoding="utf-8") as f:
        head = json.load(f)

    current_commit = head["branches"].get(head["current_branch"])
    if not current_commit:
        print("No commits yet.")
        return

    while current_commit:
        commit_file = os.path.join(".tree/objects", current_commit)
        if not os.path.exists(commit_file):
            break
        with open(commit_file, "r", encoding="utf-8") as f:
            cdata = json.load(f)
        
        print(f"Commit: {current_commit}")
        print(f"Date:   {cdata['timestamp']}\n\n    {cdata['message']}\n")
        current_commit = cdata.get("parent")

def show_status():
    if not os.path.exists(".tree"):
        print("Fatal: Not a Tree repository.")
        return

    with open(".tree/HEAD.json", "r", encoding="utf-8") as f:
        head = json.load(f)

    print(f"On branch {head['current_branch']}\n")
    statuses = get_all_file_statuses(".")
    staged = [f for f, s in statuses.items() if s == "[staged]"]
    modified = [f for f, s in statuses.items() if s == "[modified]"]
    untracked = [f for f, s in statuses.items() if s == "[untracked]"]

    if staged:
        print("Changes staged for commit:")
        for f in staged: print(f"  staged:   {f}")
        print()
    if modified:
        print("Changes not staged for commit:")
        for f in modified: print(f"  modified: {f}")
        print()
    if untracked:
        print("Untracked files:")
        for f in untracked: print(f"  untracked: {f}")
        print()
    if not staged and not modified and not untracked:
        print("Working tree clean. Nothing to commit.")

def render_tree(start_dir, prefix="", patterns=None, status_map=None):
    if patterns is None: patterns = load_ignore_patterns(start_dir)
    if status_map is None: status_map = get_all_file_statuses(start_dir)
        
    try: entries = sorted(os.listdir(start_dir))
    except PermissionError: return

    valid_entries = [e for e in entries if not is_ignored(e, patterns)]
    count = len(valid_entries)
    
    for index, entry in enumerate(valid_entries):
        path = os.path.join(start_dir, entry)
        is_last = (index == count - 1)
        connector = "└── " if is_last else "├── "
        
        if os.path.isdir(path):
            print(f"{prefix}{connector}{entry}/")
            extension = "    " if is_last else "│   "
            render_tree(path, prefix + extension, patterns, status_map)
        else:
            rel_path = os.path.relpath(path, ".").replace("\\", "/")
            file_status = status_map.get(rel_path, "")
            badge = f"  {file_status}" if file_status and file_status != "[clean]" else ""
            print(f"{prefix}{connector}{entry}{badge}")

def main():
    args = sys.argv[1:]
    is_double_clicked = len(args) == 0

    if args and args[0] in ["--help", "-h"]:
        print(f"🌳 {__APP_NAME__} v{__VERSION__} by {__AUTHOR__}")
        print("Usage:\n  tree              Display directory structure\n  tree init         Initialize repository\n  tree add <file|.> Stage file changes\n  tree commit -m    Record staged changes\n  tree status       Show working directory status\n  tree log          Show commit history log")
        return

    if args and args[0] in ["--version", "-v"]:
        print(f"🌳 {__APP_NAME__} Version {__VERSION__} (Publisher: {__AUTHOR__})")
        return

    if args:
        cmd = args[0]
        if cmd == "init": init_repo(); return
        elif cmd == "add": add_files(args[1:] if len(args) > 1 else ["."]); return
        elif cmd == "commit": 
            if len(args) >= 3 and args[1] == "-m": commit_changes(args[2])
            else: print('Usage: tree commit -m "Commit message"')
            return
        elif cmd == "log": show_log(); return
        elif cmd == "status": show_status(); return

    # Default action
    target_directory = "."
    print(os.path.abspath(target_directory))
    render_tree(target_directory)

    # Prevent immediate close if double-clicked from file explorer
    if is_double_clicked and sys.platform == "win32":
        print("\n" + "-"*40)
        try:
            input("Press Enter to exit (Run 'tree --help' in terminal for commands)...")
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()