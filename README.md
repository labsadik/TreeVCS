# TreeVCS (Tree Version Control System)

**TreeVCS** is a lightweight, intuitive, tree-structured version control system engineered for developers who need clean, visual snapshot management without the bloat of traditional version control tools. Built with a focus on fast execution, visual commit lineage, and zero-dependency standalone distribution, TreeVCS simplifies local tracking, branching, and production releases.

---

## Overview & Purpose

Modern software projects often suffer from overly complex Git workflows, detached HEAD states, and heavy overhead when all that is needed is deterministic snapshot tracking and clean workspace management.

**TreeVCS** solves this by enforcing a structural tree-based model for file history. It tracks project revisions as explicit, visual branches that mirror a logical file hierarchy. Designed as a native 64-bit Windows application, TreeVCS can be installed via a signed setup executable or run directly from source.

---

## Key Features

* **Single-Binary Portability:** Compiles into a standalone executable (`tree.exe`) with zero required Python runtime dependencies on target machines.
* **Intuitive Branching Engine:** Tracks commits in hierarchical tree nodes, making revision traversal and workspace rollbacks instantaneous.
* **Code-Signed Security:** Distributed releases are signed with Authenticode SHA256 certificates for safe Windows deployment.
* **Automated Packaging Pipeline:** Built-in support for PyInstaller and Inno Setup for rapid, repeatable single-command builds.
* **Minimal Resource Footprint:** Optimized snapshot storage engine designed for fast local operation.

---

## System Requirements & Prerequisites

| Environment | Requirement |
| --- | --- |
| **Operating System** | Windows 10 / 11 (64-bit) |
| **Python (Source Build Only)** | Python 3.11+ |
| **Build Tools (Developers)** | PyInstaller 6.x+, Inno Setup 7+ |
| **Permissions** | Standard user execution; Administrator required for global `Program Files` setup |

---

## Installation

### Option A: Standard Windows Installer (Recommended)

1. Download the latest `tree_installer_v1.0.0.exe` from the [Releases](https://www.google.com/search?q=https://github.com/labsadik/TreeVCS/releases) page.
2. Run the setup executable.
3. Follow the installation wizard prompts. The installer automatically registers `tree` into your system `PATH`.
4. Open a new PowerShell terminal and verify installation:
```powershell
tree --version

```



### Option B: Building from Source

If you prefer to compile the application executable yourself:

1. Clone the repository:
```powershell
git clone https://github.com/labsadik/TreeVCS.git
cd TreeVCS

```


2. Install dependencies (if any):
```powershell
python -m pip install --upgrade pip
pip install pyinstaller

```


3. Build the binary using PyInstaller:
```powershell
pyinstaller --onefile --name=tree --icon=scripts/app_icon.ico --version-file=version.txt --distpath=releases/v1.0.0 src/tree.py

```



---

## Setup & First-Time Configuration

After installing TreeVCS, initialize your identity before creating snapshots:

```powershell
# Set global author credentials
tree config --global user.name "user name"
tree config --global user.email "user@example.com"

```

---

## Usage Guide & Command Reference

### 1. Initialize a Repository

Navigate to your project folder and initialize tracking:

```powershell
cd C:\Users\YourUser\Projects\MyProject
tree init

```

### 2. Stage and Commit Changes

Add files to the staging index and commit them to the active node:

```powershell
# Add all files in workspace
tree add .

# Create a version commit
tree commit -m "Initial production commit for v1.0.0"

```

### 3. Inspect Status and History

Check current working tree modifications and visual commit lineage:

```powershell
# View modified, added, or deleted files
tree status

# Display visual tree graph of commits
tree log --graph

```

### 4. Branching and Navigation

Create structured branches and move across historical nodes:

```powershell
# Create a new feature branch
tree branch feature/login-system

# Switch to the feature branch
tree checkout feature/login-system

# Rollback to a specific commit ID
tree checkout c4f891a

```

---

## Project Structure

```text
TreeVCS/
├── src/
│   └── tree.py              # Main application entry point & CLI core
├── scripts/
│   ├── app_icon.ico         # Executable icon asset
│   └── installer_script.iss # Inno Setup compilation script
├── build/                   # Intermediate build artifacts
├── releases/
│   └── v1.0.0/
│       ├── tree.exe         # Compiled standalone binary
│       └── tree_installer_v1.0.0.exe  # Final signed setup wizard
├── version.txt              # Windows executable metadata
└── README.md                # Documentation

```

---

## Developer Release Pipeline

To produce a clean, signed production release:

```powershell
# 1. Clean previous build directories
Remove-Item -Recurse -Force build, dist, releases -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path releases\v1.0.0 -Force

# 2. Compile Python entry point to executable
pyinstaller --onefile --name=tree --icon=scripts/app_icon.ico --version-file=version.txt --distpath=releases/v1.0.0 src/tree.py

# 3. Compile installer package using Inno Setup
& "C:\Program Files\Inno Setup 7\ISCC.exe" "scripts\installer_script.iss"

# 4. Apply Authenticode SHA256 Signature
$cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object { $_.Subject -match "Sadik Laskar" } | Select-Object -First 1
Set-AuthenticodeSignature -FilePath "releases\v1.0.0\tree_installer_v1.0.0.exe" -Certificate $cert -HashAlgorithm SHA256

```

---

## Author & License

* **Developer:** Sadik Laskar ([@labsadik](https://www.google.com/search?q=https://github.com/labsadik))
* **Repository:** [https://github.com/labsadik/TreeVCS](https://www.google.com/search?q=https://github.com/labsadik/TreeVCS)
* **License:** Distributed under the MIT License. See `LICENSE` for details.