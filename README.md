
# TreeVCS (Tree Version Control System)

**TreeVCS** is a lightweight, intuitive, tree-structured version control system engineered for developers who need clean, visual snapshot management without the bloat of traditional version control tools. Built with a focus on fast execution, visual commit lineage, and zero-dependency standalone distribution, TreeVCS simplifies local tracking, branching, and production releases.

---

## Overview & Purpose

Modern software projects often suffer from overly complex workflows and heavy overhead when all that is needed is deterministic snapshot tracking and clean workspace management. 

**TreeVCS** solves this by enforcing a structural tree-based model for file history. It tracks project revisions as explicit, visual branches that mirror a logical file hierarchy. Designed as a native 64-bit Windows application, TreeVCS can be installed via a setup executable or run directly from source.

---

## Key Features

* **Single-Binary Portability:** Compiles into a standalone executable (`tree.exe`) with zero required Python runtime dependencies on target machines.
* **Intuitive Branching Engine:** Tracks commits in hierarchical tree nodes, making revision traversal and workspace rollbacks instantaneous.
* **Automatic Exclusions (`.treeignore`):** Automatically generates a `.treeignore` file on initialization, functioning identically to `.gitignore` to keep temporary or unwanted build files out of your snapshots.
* **Interactive Shell:** Offers a convenient dedicated command-line shell interface (`tree>`) for continuous command entry.
* **Minimal Resource Footprint:** Optimized snapshot storage engine designed for fast local operation.

---

## System Requirements & Prerequisites

| Environment | Requirement |
| --- | --- |
| **Operating System** | Windows 10 / 11 (64-bit) |
| **Python (Source Build Only)** | Python 3.11+ |
| **Build Tools (Developers)** | PyInstaller 6.x+, Inno Setup 7+ |
| **Permissions** | Standard user execution; Administrator required for global setup |

---

## Installation & Getting Started

### Option A: Standard Windows Installer (Recommended for End Users)

If you just want to download and use the tool without messing with code, follow these steps:

1. Download the latest `tree_installer_v1.0.0.exe` directly from the [Releases Page](https://github.com/labsadik/TreeVCS/releases).
2. Run the setup executable and follow the wizard instructions.
3. Open a **new** PowerShell terminal and verify your installation:
   ```powershell
   tree --version

### Option B: Cloning and Building from Source (For Developers)

If you are cloning the repository to contribute or build it yourself:

1. Clone your repository:
```powershell
git clone [https://github.com/labsadik/TreeVCS.gif](https://github.com/labsadik/TreeVCS.gif)
cd TreeVCS

```


2. Install dependencies:
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

After installing TreeVCS via the executable, configure your user identity before making snapshots:

```powershell
tree config --global user.name "Your Name"
tree config --global user.email "your.email@example.com"

```

---

## Usage Guide & Command Reference

TreeVCS can be launched interactively by simply typing `tree.exe` in your project folder, which opens the interactive shell prompt (`tree> `). Here is how to use it step-by-step with examples:

### 1. Launch the Interactive Shell

Navigate to your project folder in PowerShell and launch the tool:

```powershell
cd C:\Users\YourUser\Projects\MyProject
tree.exe

```

*(Your prompt will change to `tree> `)*

### 2. Initialize a Repository

Inside the interactive prompt, initialize tracking for your project:

```text
tree> init

```

*(This creates a `.tree/` directory and a `.treeignore` file. Files specified in `.treeignore` are automatically excluded from tracking, exactly like `.gitignore`).*

### 3. Stage and Commit Changes

Add your project files to the staging area and record a commit snapshot:

```text
# Stage changes
tree> add .

# Commit with a message
tree> commit -m "Initial production commit for v1.0.0"

```

### 4. Check Status and History

Verify your working directory state or view past commits:

```text
# View file modification status
tree> status

# Display commit history log
tree> log

```

### 5. Render Directory Tree & Exit

Display a visual layout of your directory or exit the shell:

```text
# Show directory structure
tree> tree

# Close the interactive shell
tree> exit

```

---

## VS Code Integration for `.treeignore`

To make `.treeignore` display with the proper ignore icon and syntax highlighting in VS Code, create a folder named `.vscode` in your project root and add a file named `settings.json` with the following configuration:

```json
{
  "files.associations": {
    ".treeignore": "ignore"
  },
  "git.ignoreLimitWarning": 10000,
  "git.excludeFileName": ".treeignore"
}

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
├── releases/
│   └── v1.0.0/
│       ├── tree.exe         # Compiled standalone binary
│       └── tree_installer_v1.0.0.exe  # Final setup wizard
├── version.txt              # Windows executable metadata
└── README.md                # Documentation

```

---

## Author & License

* **Developer:** Sadik Laskar ([@labsadik](https://www.google.com/search?q=https://github.com/labsadik))
* **Repository:** [https://github.com/labsadik/TreeVCS](https://github.com/labsadik/TreeVCS)
* **License:** Distributed under the MIT License. See `LICENSE` for details.
