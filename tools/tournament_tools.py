from api.tournament_api import TournamentAPI
from auth.request_context import get_access_token

api = TournamentAPI()


def register_tournament_tools(mcp):
    @mcp.tool()
    def get_my_club_tournaments(
        # content: str | None = None,
        organizationDateFrom: str | None = None,
        organizationDateTo: str | None = None,
    ):
        """
        Lấy danh sách giải đấu của hệ thống hiện tại theo phân trang.

        Get tournaments for the system with pagination.

        Parameters
        ----------

        organizationDateFrom : str | None
            Start date filter in YYYY-MM-DD format.

        organizationDateTo : str | None
            End date filter in YYYY-MM-DD format.

        Returns
        -------
        Trả về dữ liệu phân trang tournament.

        A paginated JSON response containing tournaments.
        """

        access_token = get_access_token()

        return api.get_my_club_tournaments(
            access_token=access_token,
            page=0,
            size=5,

            organizationDateFrom=organizationDateFrom,
            organizationDateTo=organizationDateTo,
        )
def find_tournament_nearby_tools(mcp):    
    @mcp.tool()
    def get_nearby_badminton_tournaments(
    ):
        """
        Lấy danh sách các giải đấu cầu lông ở gần vị trí của người dùng.

        Get a list of nearby badminton tournaments based on the user's location.


        Returns
        -------
        Trả về dữ liệu phân trang chứa danh sách giải đấu gần người dùng, có địa chỉ địa chỉ cụ thể

        A paginated JSON response containing a list of badminton tournaments nearby user, and have specific address.
        """

        access_token = get_access_token()

        return api.get_nearby_badminton_tournaments(
            access_token=access_token,  
        )