import json
import subprocess
import ast
from pathlib import Path

class AutoRefactorTool:

    def __init__(self, code_base: str):
        self.code_base = code_base
        
    def run(self):
        parsed_analysis = self.code_analyzing()
        self.refactoring_suggesting(parsed_analysis)

    @staticmethod
    def run_bandit(path):
        print('Running Bandit...')
        result = subprocess.run(
            [
                "bandit",
                "-r",
                "-ll",
                "-ii",
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

    def run_codespell(self):
        print("Running CodeBase")
        result = subprocess.run(
        [
            "codespell",
            "-s",
            self.code_base,
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
            if r == "":
                break
            filename, line_number, r = r.split(':')
            type_str, fixed_str = r.split(" ==> ")
            d[i] = {"filename": filename,
                    "line_number": line_number,
                    "code": self.extract_relevant_code(filename, int(line_number)),
                    "issue_text": f"suspected type. {type_str[1:]} should be replaced with {fixed_str}"}
   
        return d

    def code_analyzing(self):
        res = {}
        res['security_analysis'] = self.run_bandit(self.code_base)
        res['typo_analysis'] = self.run_codespell()
        return res

    def refactoring_suggesting(self, parsed_analysis):
        system_prompt = {"You are an expert Python Security & Software Engineer. Your job is to take raw Python code along with a list of static analysis issues (from Bandit and Codespell) and produce a refactored, clean version of the code that fixes all issues while preserving functional behavior"}
        user_prompt = f"Target File: {self.code_base}\n\nOriginal Code:\npython\n\n\nDetected Security Issues:\n{parsed_analysis['security_analysis']}\n\nDetected Spelling Issues:\n{parsed_analysis['typo_analysis']}Please provide the refactored code, explanations, and confidence score"

    def Summerize_analysis(self):
        pass

    def extract_relevant_code(self, filename: str, line_number: int) -> dict:
        source = Path(filename).read_text(encoding="utf-8")
        lines = source.splitlines()

        tree = ast.parse(source)

        relevant_nodes = (
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.ClassDef,
        )

        candidates = [
            node
            for node in ast.walk(tree)
            if isinstance(node, relevant_nodes)
            and node.lineno <= line_number <= node.end_lineno
        ]

        if candidates:
            node = min(
                candidates,
                key=lambda n: n.end_lineno - n.lineno
            )

            start = node.lineno
            end = node.end_lineno
        else:
            # Fallback: surrounding lines
            start = max(1, line_number - 5)
            end = min(len(lines), line_number + 5)

        return "\n".join(lines[start - 1:end])