from api.club_api import ClubAPI
from config import BASE_URL
from auth.request_context import get_access_token
api = ClubAPI()


def register_club_tools(mcp):

    @mcp.tool()
    def get_public_badminton_clubs(
        search: str | None = None,
        province: str | None = None,
        ward: str | None = None,
        selectedLevels: list[str] | None = None,
        facilityNames: list[str] | None = None,
        reputationSort: str | None = None,
    ):
        """
        Lấy danh sách các câu lạc bộ cầu lông công khai.

        Get a list of public badminton clubs from BadmintonNet.

        This tool returns a paginated list of badminton clubs.

        Parameters
        ----------
        search : str | None
            Keyword used ONLY to search by club name.
            Do NOT use this field for province, ward, facility name, or skill level.
            Use `province`, `ward`, `facilityNames`, or `selectedLevels` instead.

        province : str | None
            Province or district where the club is located.

        ward : str | None
            Ward or local administrative area.

        selectedLevels : list[str] | None
            Player skill levels supported by the club.
            Possible values:
                - "Mới tập chơi"
                - "Cơ bản"
                - "Trung bình"
                - "Trung bình khá"
                - "Khá"
                - "Bán chuyên"

        facilityNames : list[str] | None
            Filter clubs by the badminton facility (court venue) where the club operates.

            This represents the **name of the badminton court / sports facility**
            where the club usually organizes activities or training.
            Examples:
                - "Sân cầu lông Phúc An"
                - "Nhà thi đấu Dĩ An"
                - "Badminton Arena Thủ Đức"

        reputationSort : str | None
            Sort clubs by reputation.
            Possible values:
                - "asc"
                - "desc"

        Returns
        -------
        Trả về dữ liệu phân trang chứa danh sách câu lạc bộ và thông tin liên quan.

        A paginated JSON response containing a list of badminton clubs and their information.
        """

        access_token = get_access_token()

        return api.get_public_clubs(
            access_token=access_token,
            search=search,
            province=province,
            ward=ward,
            selectedLevels=selectedLevels,
            facilityNames=facilityNames,
            reputationSort=reputationSort,
        )

def join_club_tools(mcp):
    @mcp.tool()
    def join_club(club_name: str):
        """
        Tham gia một câu lạc bộ cầu lông.

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
        clubs = api.get_public_clubs(
            access_token=access_token,
            search=club_name,
        ).get("clubs", [])
        club = clubs[0] if clubs else None
        if not club:
            return {"error": "Không tìm thấy câu lạc bộ phù hợp."}

        club_id = club.get("id")
        if not club_id:
            return {"error": "Không lấy được club_id của câu lạc bộ."}

        join_result = api.join_club(
            access_token=access_token,
            club_id=club_id,
        )

        return {
            "clubId": club_id,
            "clubName": club.get("name"),
            "joinUrl": f"{BASE_URL}/my/clubs",
            "result": join_result,
        }

def find_club_nearby_tools(mcp):    
    @mcp.tool()
    def get_nearby_badminton_clubs(
    ):
        """
        Lấy danh sách các câu lạc bộ cầu lông ở gần vị trí của người dùng.

        Get a list of nearby badminton clubs based on the user's location.


        Returns
        -------
        Trả về dữ liệu phân trang chứa danh sách câu lạc bộ gần người dùng, có địa chỉ địa chỉ cụ thể

        A paginated JSON response containing a list of badminton clubs nearby user, and have specific address.
        """

        access_token = get_access_token()

        return api.get_nearby_badminton_clubs(
            access_token=access_token,  
        )
