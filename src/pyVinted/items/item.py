from datetime import datetime, timezone
from pyVinted.requester import requester


class Item:
    def __init__(self, data):
        self.raw_data = data
        self.id = data.get("id")
        self.title = data.get("title", "")
        self.brand_title = (
            data.get("brand_title")
            or (data.get("item_box") or {}).get("first_line")
            or (data.get("brand_dto") or {}).get("title")
            or "Unknown brand"
        )
        self.size_title = (
            data.get("size_title")
            or (data.get("item_box") or {}).get("second_line")
            or ""
        )
        price_info = data.get("price")
        if isinstance(price_info, dict):
            self.currency = price_info.get("currency_code", "EUR")
            self.price = price_info.get("amount", "0")
        else:
            self.currency = data.get("currency", "EUR")
            self.price = price_info or "0"

        photo_info = data.get("photo")
        if isinstance(photo_info, dict):
            self.photo = photo_info.get("url", "")
            high_res = photo_info.get("high_resolution") or {}
            self.raw_timestamp = high_res.get("timestamp")
        else:
            self.photo = photo_info or ""
            self.raw_timestamp = None

        url_path = data.get("url", "")
        if url_path and url_path.startswith("/"):
            self.url = f"https://www.vinted.fr{url_path}"
        else:
            self.url = url_path

        if self.raw_timestamp:
            try:
                self.created_at_ts = datetime.fromtimestamp(
                    self.raw_timestamp, tz=timezone.utc
                )
            except Exception:
                self.created_at_ts = datetime.now(timezone.utc)
        else:
            self.created_at_ts = datetime.now(timezone.utc)

    def __eq__(self, other):
        return self.id == getattr(other, "id", None)

    def __hash__(self):
        return hash(('id', self.id))

    def isNewItem(self, minutes=3):
        delta = datetime.now(timezone.utc) - self.created_at_ts
        return delta.total_seconds() < minutes * 60


