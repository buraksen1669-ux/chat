from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class InstagramPost:
    post_id: str
    like_count: int
    comments_count: int
    timestamp: datetime
    content_type: str
    caption: Optional[str] = None

    @property
    def total_interactions(self) -> int:
        return self.like_count + self.comments_count


@dataclass
class FollowerPoint:
    date: datetime
    follower_count: int
