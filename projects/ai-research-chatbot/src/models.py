from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional

class PaperMetadata(BaseModel):
    title: str = Field(..., min_length=1, max_length=300, description="Paper title")
    abstract: str = Field(..., min_length=10, max_length=2000, description="Paper abstract")

    @field_validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v

    @field_validator('abstract')
    def abstract_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Abstract cannot be empty')
        return v

class PaperInput(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Search query for research papers"
    )
    max_results: Optional[int] = Field(
        default=50,
        ge=1,
        le=100,
        description="Maximum number of papers to fetch"
    )

def test_validator():
    try:
        valid_input = PaperInput(query="machine learning", max_results=20)
        print(f"Valid input: {valid_input}")
    except ValidationError as e:
        print(f"Validation error: {e}")

    try:
        invalid_input = PaperInput(query="ml", max_results=200)
        print(invalid_input)
    except ValidationError as e:
        print(f"Validation error: {e}")

if __name__ == "__main__":
    test_validator()