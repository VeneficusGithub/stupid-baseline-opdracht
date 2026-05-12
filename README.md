# Student Python Project
 
A minimal Python project template using **uv** for dependency and environment management.
 
## Installation & Setup
 
### 1. Install uv
 
**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
 
**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.sh | iex"
```
 
### 2. Clone this repository
```bash
git clone <repository-url>
cd <project-name>
```
 
### 3. Run the example
```bash
uv run python src/main.py
```
 
That's it! You're ready to code.
 
---
 
## How to Use
 
### Run Your Code
```bash
uv run python src/main.py
```
 
No need to activate anything—`uv` handles the virtual environment automatically.
 
### Add a Package
```bash
# For regular dependencies
uv add requests
 
# For dev-only tools (testing, formatting, etc.)
uv add --dev pytest
```
 
### Run Tests
```bash
uv run pytest
```
 
### Check Your Dependencies
```bash
uv pip list
```
 
---
 
## File Structure
 
```
.
├── src/
│   └── main.py          # Your code goes here
├── tests/               # Optional: test files
├── pyproject.toml       # Project metadata & dependencies
├── uv.lock              # Auto-generated: locked versions
├── .python-version      # Python version (3.12)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```
 
---
 
## Understanding uv
 
**What is uv?** A super-fast Python package and environment manager written in Rust.
 
**Why use it?**
- ✅ Incredibly fast (10-100x faster than pip)
- ✅ Single command for everything (no more `pip`, `venv`, `pip-tools`)
- ✅ Automatic virtual environment management
- ✅ Reproducible: `uv.lock` guarantees same versions everywhere
- ✅ Simple: Just `uv run` instead of `source venv/bin/activate && python ...`
 
**Key differences from pip:**
- No manual `python -m venv` needed
- No need to activate/deactivate environments
- Dependencies lock automatically
- Much faster installation
 
---
 
## Common Tasks
 
### Install a specific version
```bash
uv add "flask>=2.3.0,<3.0"
```
 
### Remove a package
```bash
uv remove requests
```
 
### Update all packages
```bash
uv lock --upgrade
```
 
### See what's installed
```bash
uv pip list
```
 
---
 
## Tips for Students
 
1. **Always commit `uv.lock`** to version control—it ensures everyone has the same dependencies.
 
2. **Use dev dependencies** for testing tools:
   ```bash
   uv add --dev pytest black ruff
   ```
 
3. **Don't commit `.venv`**—it's auto-generated. It's in `.gitignore` by default.
 
4. **Check `.python-version`** if something seems off. Edit it to change Python versions.
 
5. **Still prefer activating the venv?** You can:
   ```bash
   # Activate (optional—not needed for uv run)
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```
 
---
 
## Troubleshooting
 
| Problem | Solution |
|---------|----------|
| `uv: command not found` | Restart your terminal after installing uv |
| Wrong Python version | Edit `.python-version` and run `uv sync` |
| Dependencies seem stale | Run `uv sync` to refresh |
| Want to clean up? | Delete `.venv` folder; it regenerates automatically |
 
---
 
## Learn More
 
- [uv Documentation](https://docs.astral.sh/uv/)
- [Getting Started with uv](https://docs.astral.sh/uv/getting-started/)
- [Managing Projects with uv](https://docs.astral.sh/uv/guides/projects/)
 
---\
 
**Happy coding! 🚀**