from pydantic import BaseModel, Field
from typing import List, Optional


class Videos(BaseModel):
    key: str
    type: str

class Movie(BaseModel):
    unique_id: int
    title: str
    original_language: Optional[str]
    overview: Optional[str]
    media_type: str
    genres: list[str]
    release_date: str
    budget: int
    imdb_id: Optional[str]
    imdb_rating: Optional[float]
    production_companies: list[str]
    revenue: Optional[int]
    runtime: Optional[int]
    spoken_languages: Optional[list[str]]
    status: str
    team: Optional[dict]
    cast_details: Optional[list[str]]
    reviews: Optional[list]
    images: Optional[list[str]]
    keywords: Optional[list[str]]
    videos: list[Videos]
    plot: str