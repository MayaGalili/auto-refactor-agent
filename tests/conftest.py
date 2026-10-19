import json
from pathlib import Path

import pytest

from src.schemas import CodeReviewResult


@pytest.fixture
def llm_results():
    fixture_path = (
        Path(__file__).parent
        / "fixtures"
        / "llm_responses.json"
    )

    data = json.loads(
        fixture_path.read_text(encoding="utf-8")
    )

    return {
        filename: CodeReviewResult.model_validate(result)
        for filename, result in data.items()
    }