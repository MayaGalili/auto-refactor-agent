import pytest
from src.analyzer import AutoRefactorTool

class TestAutoRefactor:

    def test_run_codespell(self):
        a = AutoRefactorTool( "/Users/maya/projects/auto-refactor-agent/examples").run_codespell()
        assert isinstance(a, dict)


