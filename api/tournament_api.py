import requests
from config import BASE_URL


class TournamentAPI:
    def get_my_club_tournaments(
        self,
        access_token: str | None = None,
        page: int = 0,
        size: int = 5,
        # content: str | None = None,
        organizationDateFrom: str | None = None,
        organizationDateTo: str | None = None,
    ):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        params = {
            "page": page,
            "size": size,
        }

        # if content:
        #     params["content"] = content

        if organizationDateFrom:
            params["organizationDateFrom"] = organizationDateFrom

        if organizationDateTo:
            params["organizationDateTo"] = organizationDateTo

        res = requests.get(
            f"{BASE_URL}/tournaments",
            params=params,
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()

        raw = res.json()

        # 🔥 FILTER RESPONSE CHO MCP
        tournaments = raw.get("data", {}).get("content", [])

        slim = []
        for t in tournaments:
            slim.append({
                "id": t.get("id"),
                "name": t.get("name"),
                "location": t.get("location"),
                "startDate": t.get("startDate"),
                "endDate": t.get("endDate"),
                "status": t.get("status"),
                "slug": t.get("slug"),
                "url": f"/tournaments/{t.get('slug')}" if t.get("slug") else None,
            })

        return {
            "tournaments": slim,
            "page": raw["data"]["page"],
            "totalPages": raw["data"]["totalPages"],
        }
    def get_nearby_badminton_tournaments(
        self,
        access_token: str | None = None,
    ):
        headers = {}

        res = requests.get(
            f"{BASE_URL}/club-event/nearby",
            headers=headers
        )

        res.raise_for_status()
        return res.json()
