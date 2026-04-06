import requests
from config import BASE_URL


def _normalize_local_datetime(value: str, is_end: bool = False) -> str:
    """Convert YYYY-MM-DD to ISO LocalDateTime expected by backend."""
    if "T" in value:
        return value

    date_part = value.strip()

    if len(date_part) == 10 and date_part[4] == "-" and date_part[7] == "-":
        return f"{date_part}T23:59:59" if is_end else f"{date_part}T00:00:00"

    return value


class ClubEventAPI:
    def get_public_club_events(
        self,
        access_token: str | None = None,
        page: int = 0,
        size: int = 5,
        search: str | None = None,
        province: str | None = None,
        ward: str | None = None,
        quickTimeFilter: str | None = None,
        isFree: bool | None = None,
        minFee: float | None = None,
        maxFee: float | None = None,
        startDate: str | None = None,
        endDate: str | None = None,
        advancedFilter: dict | None = None,
    ):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        params = {
            "page": page,
            "size": size,
        }

        if search:
            params["search"] = search

        if province:
            params["province"] = province

        if ward:
            params["ward"] = ward

        if quickTimeFilter:
            params["quickTimeFilter"] = quickTimeFilter

        if isFree is not None:
            params["isFree"] = isFree

        if minFee is not None:
            params["minFee"] = minFee

        if maxFee is not None:
            params["maxFee"] = maxFee

        if startDate:
            params["startDate"] = _normalize_local_datetime(startDate)

        if endDate:
            params["endDate"] = _normalize_local_datetime(endDate, is_end=True)

        payload = advancedFilter if advancedFilter is not None else None

        res = requests.post(
            f"{BASE_URL}/club-event/all/public",
            params=params,
            json=payload,
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()

        raw = res.json()

        events = raw.get("data", {}).get("content", [])

        slim = []

        for e in events:
            slim.append({
                "id": e.get("id"),
                "title": e.get("title"),
                "slug": e.get("slug"),
                "location": e.get("location")
                    or (e.get("facility") or {}).get("location"),
                "facilityName": (e.get("facility") or {}).get("name"),
                "startTime": e.get("startTime"),
                "endTime": e.get("endTime"),
                "fee": e.get("fee"),
                "totalSlot": e.get("totalMember"),
                "joinedSlot": e.get("joinedMember"),
                "clubName": e.get("nameClub"),
                "categories": e.get("categories"),
                "status": e.get("status"),
                # ⭐ bonus giúp render link chắc chắn
                "url": f"/events/{e.get('slug')}" if e.get("slug") else None,
            })

        return {
            "events": slim,
            "page": raw["data"]["page"],
            "totalPages": raw["data"]["totalPages"],
            "last": raw["data"]["last"],
        }
    def join_event(
        self,
        access_token: str,
        event_id: str,
        
    ):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }


        res = requests.post(
            f"{BASE_URL}/club-event/join/{event_id}",
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()

        return res.json()
    
    def get_nearby_club_events(
        self,
        access_token: str,
    ):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        res = requests.get(
            f"{BASE_URL}/club-event/nearby",
            headers=headers
        )

        res.raise_for_status()
        return res.json()