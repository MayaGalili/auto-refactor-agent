import json
import subprocess

class AutoRefactorTool:

    def __init__(self, code_base: str):
        self.code_base = code_base
        
    def run(self):
        self.code_analyzing()

    @staticmethod
    def run_bandit(path):
        result = subprocess.run(
            [
                "bandit",
                "-r",
                path,
                "-f",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        if not result.stdout:
            raise RuntimeError(
                f"Bandit failed to run:\n{result.stderr}"
            )

        return json.loads(result.stdout)

    def run_codespell(self):
        pass

    def code_analyzing(self):
        self.run_bandit(self.code_base)

    def refactoring_suggesting(self):
        pass

    def Summerize_analysis(self):
        pass