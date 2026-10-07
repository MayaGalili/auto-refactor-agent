import json
import subprocess
import sys

class AutoRefactorTool:

    def __init__(self, code_base: str):
        self.code_base = code_base
        
    def run(self):
        self.code_analyzing()

    def code_analyzing(self):


        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "bandit",
                "-r",
                self.code_base,
                "-f",
                "json",
            ],
            capture_output=True,
            text=True,
        )
        print("return code:", result.returncode)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)

        return json.loads(result.stdout)

    def refactoring_suggesting(self):
        pass

    def Summerize_analysis(self):
        pass