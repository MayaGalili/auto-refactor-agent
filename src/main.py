import argparse
from pathlib import Path

from src.analyzer import AutoRefactorTool

DEFAULT_CODE_BASE = Path(__file__).parent.parent / "examples"


def main(code_base):
    print(f"Starting Code Base analyzing for code base:\n {code_base}")
    AutoRefactorTool(code_base).run()
    print("The code base analysis is done!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scan a Python code base with bandit and codespell, "
                    "get LLM refactoring suggestions and apply the approved ones."
    )
    parser.add_argument(
        "code_base",
        nargs="?",
        default=str(DEFAULT_CODE_BASE),
        help="Path to the directory to analyze (default: the bundled examples/ directory)",
    )
    args = parser.parse_args()
    main(args.code_base)
