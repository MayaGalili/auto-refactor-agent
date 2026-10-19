from pydantic import BaseModel

class CodeFix(BaseModel):
    issue_codes: list[str]
    explanation: str
    original_code: str
    suggested_code: str


class CodeReviewResult(BaseModel):
    fixes: list[CodeFix]
    unresolved_issues: list[str]