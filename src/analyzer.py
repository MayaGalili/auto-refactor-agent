import json
import subprocess

class AutoRefactorTool:

    def __init__(self, code_base: str):
        self.code_base = code_base
        
    def run(self):
        self.code_analyzing()

    @staticmethod
    def run_bandit(path):
        print('Running Bandit...')
        result = subprocess.run(
            [
                "bandit",
                "-r",
                "-ll",
                "-ii",
                # "--format",
                # "custom",
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

        res = json.loads(result.stdout)
        res = res['results']
        wanted_keys = ["filename", "line_number", "code", "issue_text"]
        d = dict()
        for i, n in enumerate(res):
            d[i] = {key: n[key] for key in wanted_keys}

        print(d)
        return d 

    @staticmethod
    def run_codespell(path):
        print("Running CodeBase")
        result = subprocess.run(
        [
            "codespell",
            "-s",
            path,
        ],
        capture_output=True,
        text=True,
    )
        if not result.stdout:
            raise RuntimeError(
                f"CodeSpell failed to run:\n{result.stderr}"
            )
        res = result.stdout
        res = res.split('\n')
        d = dict()
        for i, r in enumerate(res):
            filename, line_number, r = r.split(':')
            type_str, fixed_str = r.split(" ==> ")
            d[i] = {"filename": filename,
                    "line_number": line_number,
                    "code": "",
                    "issue_text": f"suspected type. {type_str[1:]} should be replaced with {fixed_str}"}
   
        return res

    def code_analyzing(self):
        bandit_res = self.run_bandit(self.code_base)
        # issue_text, filename, line_number

        codespell_res = self.run_codespell(self.code_base)

    def refactoring_suggesting(self):
        pass

    def Summerize_analysis(self):
        pass


    '/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:23: expcted ==> expected\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:24: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:25: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:26: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:26: expcted ==> expected\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:30: expcted ==> expected\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:31: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:32: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:33: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:33: expcted ==> expected\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:36: expcted ==> expected\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:37: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:38: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:39: ans ==> and\n/Users/maya/projects/auto-refactor-agent/examples/LeetCode3.py:39: expcted ==> expected\n\n-------8<-------\nSUMMARY:\nans           9\nexpcted       6\n'
    codespell