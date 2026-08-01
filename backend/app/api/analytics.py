from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter()


class AnalyticsResponse(BaseModel):
    total_documents: int
    by_type: dict
    by_category: dict
    engagement: dict


# Simulated analytics
_mock_engagement = {
    "views": 12500, "shares": 890, "avg_read_time": 245,
    "bounce_rate": 0.32, "conversion_rate": 0.08
}


@router.get("/", response_model=AnalyticsResponse)
async def get_analytics():
    return {
        "total_documents": 156,
        "by_type": {"article": 89, "blog_post": 45, "social": 22},
        "by_category": {"technology": 62, "business": 38, "health": 28, "science": 18, "finance": 10},
        "engagement": _mock_engagement
    }


@router.get("/engagement")
async def get_engagement():
    return {"data": _mock_engagement}
