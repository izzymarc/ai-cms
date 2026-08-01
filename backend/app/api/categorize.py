from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Keyword-based classification (simulated ML pipeline)
CATEGORY_KEYWORDS = {
    "technology": ["software", "code", "ai", "api", "cloud", "devops", "data"],
    "business": ["revenue", "startup", "funding", "strategy", "market"],
    "health": ["health", "medical", "clinical", "patient", "disease"],
    "science": ["research", "study", "experiment", "hypothesis", "lab"],
    "finance": ["investment", "stock", "market", "portfolio", "trading"],
}


class CategorizeRequest(BaseModel):
    title: str
    body: str


class CategorizeResponse(BaseModel):
    categories: List[dict]  # {name, confidence}
    tags: List[str]


@router.post("/", response_model=CategorizeResponse)
async def categorize_content(req: CategorizeRequest):
    """Categorize content using keyword extraction (simulated ML)"""
    text = f"{req.title} {req.body}".lower()
    category_scores = []

    for cat, keywords in CATEGORY_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches > 0:
            confidence = min(round(matches / len(keywords), 2), 1.0)
            category_scores.append({"name": cat, "confidence": confidence})

    category_scores.sort(key=lambda x: x["confidence"], reverse=True)

    # Extract tags from body
    words = req.body.lower().split()
    common_words = {"the", "a", "an", "and", "or", "but", "in", "on",
                    "at", "to", "for", "of", "with", "is", "are", "was", "were"}
    word_freq = {}
    for w in words:
        w = w.strip(".,!?()[]{}\"'")
        if len(w) > 4 and w not in common_words:
            word_freq[w] = word_freq.get(w, 0) + 1
    tags = [w for w, c in sorted(
        word_freq.items(), key=lambda x: x[1], reverse=True)[:8]]

    return CategorizeResponse(categories=category_scores, tags=tags)
