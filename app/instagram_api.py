from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

import requests

from app.models import FollowerPoint, InstagramPost


class InstagramAPIError(RuntimeError):
    pass


class InstagramGraphClient:
    BASE_URL = "https://graph.facebook.com/v20.0"

    def __init__(self, access_token: str, ig_user_id: str) -> None:
        self.access_token = access_token
        self.ig_user_id = ig_user_id

    def _get(self, endpoint: str, params: Optional[dict] = None) -> Dict:
        query = params or {}
        query["access_token"] = self.access_token
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, params=query, timeout=20)
            response.raise_for_status()
            payload = response.json()
            if "error" in payload:
                raise InstagramAPIError(payload["error"].get("message", "Unknown API error"))
            return payload
        except requests.RequestException as exc:
            raise InstagramAPIError(f"Instagram API isteği başarısız: {exc}") from exc

    def get_profile(self) -> Dict:
        return self._get(f"{self.ig_user_id}", params={"fields": "username,followers_count"})

    def get_recent_posts(self, limit: int = 50) -> List[InstagramPost]:
        fields = "id,caption,media_type,media_product_type,timestamp,like_count,comments_count"
        payload = self._get(
            f"{self.ig_user_id}/media",
            params={"fields": fields, "limit": min(limit, 50)},
        )

        posts: List[InstagramPost] = []
        for item in payload.get("data", []):
            try:
                post = InstagramPost(
                    post_id=item["id"],
                    like_count=int(item.get("like_count", 0)),
                    comments_count=int(item.get("comments_count", 0)),
                    timestamp=datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00")),
                    content_type=self._normalize_content_type(
                        item.get("media_type", ""), item.get("media_product_type", "")
                    ),
                    caption=item.get("caption"),
                )
                posts.append(post)
            except (KeyError, ValueError, TypeError):
                continue
        return posts

    def get_follower_growth(self) -> List[FollowerPoint]:
        endpoint = f"{self.ig_user_id}/insights"
        payload = self._get(endpoint, params={"metric": "follower_count", "period": "day"})

        points: List[FollowerPoint] = []
        for metric in payload.get("data", []):
            for value in metric.get("values", []):
                end_time = value.get("end_time")
                count = value.get("value")
                if not end_time or count is None:
                    continue
                try:
                    points.append(
                        FollowerPoint(
                            date=datetime.fromisoformat(end_time.replace("Z", "+00:00")),
                            follower_count=int(count),
                        )
                    )
                except (ValueError, TypeError):
                    continue

        points.sort(key=lambda p: p.date)
        return points

    @staticmethod
    def _normalize_content_type(media_type: str, media_product_type: str) -> str:
        if media_product_type.upper() == "REELS":
            return "Reels"
        if media_type.upper() == "IMAGE":
            return "Fotoğraf"
        if media_type.upper() == "VIDEO":
            return "Video"
        return "Diğer"
