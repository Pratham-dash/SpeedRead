"""
Request/Response Schemas
Pydantic models for API validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any


class ProcessTextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000000,
        description="Text to be processed for speed reading"
    )
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v


class CalculateORPRequest(BaseModel):
    word: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Word to calculate ORP for"
    )
    
    @validator('word')
    def validate_word(cls, v):
        if not v.strip():
            raise ValueError('Word cannot be empty or whitespace only')
        return v


class ORPData(BaseModel):
    word: str = Field(description="The original word")
    before: str = Field(description="Characters before ORP")
    orp: str = Field(description="The ORP character")
    after: str = Field(description="Characters after ORP")
    position: int = Field(ge=0, description="ORP position (1-indexed)")


class ProcessingStats(BaseModel):
    """Statistics about text processing"""
    original_count: int = Field(ge=0, description="Original word count")
    processed_count: int = Field(ge=0, description="Processed word count (with duplicates/pauses)")
    estimated_time_300wpm: float = Field(ge=0, description="Estimated reading time at 300 WPM (seconds)")
    estimated_time_500wpm: float = Field(ge=0, description="Estimated reading time at 500 WPM (seconds)")


class ProcessTextResponse(BaseModel):
    success: bool = Field(description="Whether processing was successful")
    words: List[str] = Field(description="Processed word array")
    orp_data: List[ORPData] = Field(description="ORP information for each word")
    stats: ProcessingStats = Field(description="Processing statistics")


class CalculateORPResponse(BaseModel):
    success: bool = Field(description="Whether calculation was successful")
    word: str = Field(description="The original word")
    before: str = Field(description="Characters before ORP")
    orp: str = Field(description="The ORP character")
    after: str = Field(description="Characters after ORP")
    orp_position: int = Field(ge=0, description="ORP position (1-indexed)")


class ErrorResponse(BaseModel):
    error: str = Field(description="Error type")
    message: str = Field(description="Human-readable error message")
    status: Optional[int] = Field(None, description="HTTP status code")


class HealthResponse(BaseModel):
    status: str = Field(description="Service health status")
    service: str = Field(description="Service name")
    version: str = Field(description="Service version")


# Future schemas (commented out until features are implemented)

# class ExtractURLRequest(BaseModel):
#     """Request schema for URL extraction"""
#     url: str = Field(..., description="URL to extract article from")
#     
#     @validator('url')
#     def validate_url(cls, v):
#         """Validate URL format"""
#         import re
#         pattern = re.compile(r'^https?://')
#         if not pattern.match(v):
#             raise ValueError('Invalid URL format')
#         return v


# class UploadPDFResponse(BaseModel):
#     """Response schema for PDF upload"""
#     text: str = Field(description="Extracted text from PDF")
#     pages: int = Field(ge=1, description="Number of pages")
#     metadata: Dict[str, Any] = Field(description="PDF metadata")
