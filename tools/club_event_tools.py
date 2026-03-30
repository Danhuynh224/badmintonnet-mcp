from api.club_event_api import ClubEventAPI
from auth.request_context import get_access_token
from config import BASE_URL
api = ClubEventAPI()


def register_club_event_tools(mcp):
    @mcp.tool()
    def get_public_club_events(
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
        """
        Lấy danh sách các sự kiện hoặc hoạt động công khai của câu lạc bộ.

        Get a paginated list of public club events or activities from BadmintonNet.


        Parameters
        ----------

        search : str | None
            Keyword used to search activity or event names.
            If other fields are provided, this is not required.


        province : str | None
            Province where the event takes place.

        ward : str | None
            Ward where the event takes place.

        quickTimeFilter : str | None
            Backend-defined quick time filter.

        isFree : bool | None
            Filter free or paid events.

        minFee : float | None
            Minimum participation fee.

        maxFee : float | None
            Maximum participation fee.

        startDate : str | None
            Start time filter. You can pass:
            - Date only: 2026-03-15 (auto-converted to 2026-03-15T00:00:00)
            - Full LocalDateTime: 2026-03-15T08:00:00

        endDate : str | None
            End time filter. You can pass:
            - Date only: 2026-03-20 (auto-converted to 2026-03-20T23:59:59)
            - Full LocalDateTime: 2026-03-20T21:00:00

        advancedFilter : dict | None
            Extra JSON body for the backend advanced filter request.

        Returns
        -------
        Trả về dữ liệu phân trang chứa danh sách sự kiện/hoạt động công khai.

        A paginated JSON response containing public club events or activities.
        """

        access_token = get_access_token()

        return api.get_public_club_events(
            access_token=access_token,
            page=0,
            size=5,
            search=search,
            province=province,
            ward=ward,
            quickTimeFilter=quickTimeFilter,
            isFree=isFree,
            minFee=minFee,
            maxFee=maxFee,
            startDate=startDate,
            endDate=endDate,
            advancedFilter=advancedFilter,
        )
    
def join_event_tools(mcp):
    @mcp.tool()
    def join_event(event_name: str):
        """
        Tham gia một sự kiện (hoạt động) câu lạc bộ cầu lông.

        Join a badminton club on BadmintonNet.

        Parameters
        ----------
        club_name : str
            Tên của câu lạc bộ mà người dùng muốn tham gia.
            The name of the club that the user wants to join.

        Returns
        -------
        Trả về kết quả của việc tham gia câu lạc bộ, có thể là thành công hoặc lỗi.

        The result of the join club action, which can be success or error.
        """

        access_token = get_access_token()
        events = api.get_public_club_events(
            access_token=access_token,
            search=event_name,
        ).get("events", [])
        event = events[0] if events else None
        if not event:
            return {"error": "Không tìm thấy sự kiện phù hợp."}

        event_id = event.get("id")
        if not event_id:
            return {"error": "Không lấy được event_id của sự kiện."}

        join_result = api.join_event(
            access_token=access_token,
            event_id=event_id,
        )

        return {
            "eventId": event_id,
            "eventName": event.get("title"),
            "joinUrl": f"{BASE_URL}/my/events",
            "result": join_result,
        }

def find_event_nearby_tools(mcp):
    @mcp.tool()
    def get_nearby_club_events(
       
    ):
        """
        Lấy danh sách các sự kiện hoặc hoạt động công khai của câu lạc bộ gần người dùng.

        Get a paginated list of public club events or activities nearby user from BadmintonNet.

        Returns
        -------
        Trả về dữ liệu phân trang chứa danh sách sự kiện/hoạt động công khai
        gần người dùng.
        A paginated JSON response containing public club events or activities nearby user.
        """

        access_token = get_access_token()

        return api.get_nearby_club_events(
            access_token=access_token,
        )
