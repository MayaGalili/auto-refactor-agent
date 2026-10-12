import pytest
from src.analyzer import AutoRefactorTool

class TestAutoRefactor:

    def test_run_codespell(self):
        a = AutoRefactorTool.run_codespell( "/Users/maya/projects/auto-refactor-agent/examples")


