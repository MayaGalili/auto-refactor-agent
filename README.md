# auto-refactor-agent

Automated Code Refactoring & Security Agent.

`auto-refactor-agent` scans a Python code base for security issues and typos,
asks an LLM for minimal fixes, and lets you review and approve each change
before it is written to disk.

## How it works

```
Target Python directory
        │
        ▼
Static analysis           bandit (security) + codespell (typos)
        │
        ▼
Parse & group issues      issues grouped per file, with the surrounding code
        │
        ▼
LLM suggestions           OpenAI (gpt-4.1) returns structured fixes per file
        │
        ▼
Interactive review        diff shown for each fix → you approve with y / N
        │
        ▼
Apply fixes               file backed up as <file>.bak, then updated in place
```

Every fix is applied only if the original code appears **exactly once** in the
file and the result is still valid Python — otherwise it is skipped.

## Requirements

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Installation

```bash
git clone https://github.com/MayaGalili/auto-refactor-agent.git
cd auto-refactor-agent

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

This installs the analysis tools (`bandit`, `codespell`) into the virtual
environment, so keep it **activated** whenever you run the tool or the tests.

## Configuration

Create a `.env` file in the project root with your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

On startup the tool prints `API key loaded: True` if the key was found.

## Usage

Run from the project root (with the virtual environment activated):

```bash
python -m src.main /path/to/your/python/project
```

If no path is given, the bundled `examples/` directory is analyzed:

```bash
python -m src.main
```

Run `python -m src.main --help` to see all options.

### Reviewing the suggestions

For every file with issues, the tool shows each suggested fix as a diff and
asks for confirmation:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: examples/flask_debug.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Suggested fix #0
--- Original
+++ Refactored
@@ -1 +1 @@
-app.run(debug=True)
+app.run()

Apply suggested changes? [y/N]:
```

- `y` / `yes` — apply the fix
- `n` / `no` / Enter — skip it

### Backups and undoing changes

> **Note:** approved fixes modify your files **in place**.

Before a file is changed, a copy is saved next to it as `<file>.bak`
(for example `app.py` → `app.py.bak`). To undo the changes to a file:

```bash
mv app.py.bak app.py
```

Using version control (git) on the target project is still recommended, so
you can review all changes with `git diff`. `*.bak` files are ignored by this
repository's `.gitignore`.

## Running the tests

```bash
pytest
```

The tests use recorded LLM responses (`tests/fixtures/llm_responses.json`),
so they **do not call the OpenAI API** and need no API key.
`test_apply_suggestions` runs the refactoring on a temporary copy of
`examples/`, so the original example files are never modified. The temporary
folder is kept only if the test fails, for inspection.

## Project structure

```
auto-refactor-agent/
├── src/
│   ├── main.py          # command-line entry point
│   ├── analyzer.py      # AutoRefactorTool: analysis, LLM calls, applying fixes
│   └── schemas.py       # Pydantic models for the LLM's structured output
├── examples/            # sample Python files with known issues
├── tests/
│   ├── conftest.py      # shared fixtures
│   ├── fixtures/        # recorded LLM responses
│   └── test_auto_refactor.py
├── pytest.ini
└── requirements.txt
```

## License

MIT — see [LICENSE](LICENSE).
