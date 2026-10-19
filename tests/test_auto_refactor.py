from src.analyzer import AutoRefactorTool
from src.schemas import CodeReviewResult, CodeFix

def test_bla():
    assert True

def test_run_codespell():
    a = AutoRefactorTool( "/Users/maya/projects/auto-refactor-agent/examples").run_codespell()
    assert isinstance(a, dict)

def test_apply_suggestions(llm_results):
    print("bla")
    AutoRefactorTool('').apply_suggestions(llm_results)

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


