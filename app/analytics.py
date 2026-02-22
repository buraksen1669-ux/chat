from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Dict, List, Tuple

from app.models import InstagramPost


def calculate_engagement_rate(post: InstagramPost, follower_count: int) -> float:
    if follower_count <= 0:
        return 0.0
    return (post.like_count + post.comments_count) / follower_count


def top_posts_by_engagement(posts: List[InstagramPost], follower_count: int, top_n: int = 10) -> List[Tuple[InstagramPost, float]]:
    ranked = [(post, calculate_engagement_rate(post, follower_count)) for post in posts]
    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:top_n]


def hourly_engagement(posts: List[InstagramPost], follower_count: int) -> Dict[int, float]:
    buckets: Dict[int, List[float]] = defaultdict(list)
    for post in posts:
        buckets[post.timestamp.hour].append(calculate_engagement_rate(post, follower_count))

    return {hour: mean(values) for hour, values in buckets.items()}


def content_type_engagement(posts: List[InstagramPost], follower_count: int) -> Dict[str, float]:
    buckets: Dict[str, List[float]] = defaultdict(list)
    for post in posts:
        buckets[post.content_type].append(calculate_engagement_rate(post, follower_count))

    return {content_type: mean(values) for content_type, values in buckets.items()}
