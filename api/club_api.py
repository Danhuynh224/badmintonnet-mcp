import requests
from config import BASE_URL


class ClubAPI:

    def get_public_clubs(
        self,
        access_token: str | None = None,
        search=None,
        province=None,
        ward=None,
        selectedLevels=None,
        facilityNames=None,
        reputationSort=None,
    ):
        headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        params = {
            "page": 0,
            "size": 5,
        }

        if search:
            params["search"] = search

        if province:
            params["province"] = province

        if ward:
            params["ward"] = ward

        if selectedLevels:
            params["selectedLevels"] = selectedLevels

        if facilityNames:
            params["facilityNames"] = facilityNames

        if reputationSort:
            params["reputationSort"] = reputationSort

        res = requests.get(
            f"{BASE_URL}/clubs/all_public",
            params=params,
            headers=headers,
            timeout=10
        )

        res.raise_for_status()

        raw = res.json()

        clubs = raw.get("data", {}).get("content", [])

        slim = []

        for c in clubs:
            slim.append({
                "id": c.get("id"),
                "name": c.get("name"),
                "slug": c.get("slug"),
                "location": c.get("location")
                    or (c.get("facility") or {}).get("location"),
                "facilityName": (c.get("facility") or {}).get("name"),
                "memberCount": c.get("memberCount"),
                "maxMembers": c.get("maxMembers"),
                "totalEvent": c.get("totalEvent"),
                "tags": c.get("tags"),
                "status": c.get("status"),
                # ⭐ bonus giúp LLM render link chắc chắn
                "url": f"/clubs/{c.get('slug')}" if c.get("slug") else None,
            })

        return {
            "clubs": slim,
            "page": raw["data"]["page"],
            "totalPages": raw["data"]["totalPages"],
            "last": raw["data"]["last"],
        }

    def join_club(
        self,
        access_token: str,
        club_id: str,
        
    ):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        payload = {
            "notification": "Tôi muốn tham gia câu lạc bộ của bạn trên BadmintonNet!",
        }

        res = requests.post(
            f"{BASE_URL}/clubs/{club_id}/join",
            json=payload,
            headers=headers,
            timeout=10,
        )

        res.raise_for_status()

        return res.json()
    
    def get_nearby_badminton_clubs(
        self,
        access_token: str,
    ):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        res = requests.get(
            f"{BASE_URL}/clubs/nearby",
            headers=headers
        )

        res.raise_for_status()
        return res.json()