import shutil
import tempfile
from pathlib import Path

from src.analyzer import AutoRefactorTool
from src.schemas import CodeReviewResult, CodeFix

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def test_run_codespell():
    a = AutoRefactorTool( "/Users/maya/projects/auto-refactor-agent/examples").run_codespell()
    assert isinstance(a, dict)

def test_apply_suggestions(llm_results, monkeypatch):
    # Work on a copy of the examples so the originals are never modified
    temp_dir = Path(tempfile.mkdtemp(prefix="auto_refactor_test_"))
    temp_examples = temp_dir / "examples"
    shutil.copytree(EXAMPLES_DIR, temp_examples)

    # Point the suggestions at the copied files instead of the originals
    temp_results = {
        str(temp_examples / Path(filename).relative_to(EXAMPLES_DIR)): result
        for filename, result in llm_results.items()
    }

    # Auto-approve every suggested change instead of prompting for input
    monkeypatch.setattr(AutoRefactorTool, "confirm_changes", lambda self: True)

    AutoRefactorTool(str(temp_examples)).apply_suggestions(temp_results)

    for filename in temp_results:
        refactored = Path(filename)
        backup = refactored.with_suffix(refactored.suffix + ".bak")

        assert backup.exists(), f"Missing backup for {refactored.name}"
        assert refactored.read_text(encoding="utf-8") != backup.read_text(encoding="utf-8"), (
            f"{refactored.name} was not changed by the refactoring"
        )

    # Only reached if all assertions passed - otherwise keep it for inspection
    shutil.rmtree(temp_dir)

def test_llm_results_structure(llm_results):
    assert len(llm_results) == 3

    for filename, result in llm_results.items():
        assert isinstance(filename, str)
        assert isinstance(result, CodeReviewResult)

        for fix in result.fixes:
            assert isinstance(fix, CodeFix)
            assert fix.original_code
            assert fix.suggested_code

def test_flask_debug_fix(llm_results):
    result = next(
        result
        for filename, result in llm_results.items()
        if filename.endswith("flask_debug.py")
    )

    assert len(result.fixes) == 1

    fix = result.fixes[0]

    assert fix.original_code == "app.run(debug=True)"
    assert fix.suggested_code == "app.run()"


