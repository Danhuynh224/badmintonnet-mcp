from api.profile_api import ProfileAPI
from auth.request_context import get_access_token

api = ProfileAPI()


def register_profile_tools(mcp):
    @mcp.tool()
    def get_my_profile_data():
        """
        Get personal profile data of the current authenticated user, answered for question who am i.

        Endpoint
        --------
        GET /account

        Returns only the `data` object from API response.

        Field meanings in `data`
        ------------------------
        id : str
            Unique user identifier (UUID).
        email : str
            Account email.
        fullName : str
            Full name displayed on profile.
        birthDate : str
            Birth date in YYYY-MM-DD format.
        gender : str
            Gender value (for example: MALE, FEMALE, OTHER).
        address : str
            User address.
        bio : str
            User self-introduction.
        avatarUrl : str
            URL to profile avatar image.
        phone : str
            Contact phone number.
        enabled : bool
            Whether account is active.
        createdAt : str
            Account creation timestamp (ISO-8601).
        updatedAt : str
            Latest account update timestamp (ISO-8601).
        createdBy : str
            Actor who created this account record.
        updatedBy : str
            Actor who last updated this account record.
        reputationScore : int
            Reputation/credibility score of the user.
        totalParticipatedEvents : int
            Number of events the user has joined.
        ownerClubs : list[dict]
            Clubs this user owns/manages.
            Item fields:
            - clubName: club display name
            - slug: club unique slug
            - urlLogo: club logo URL
        myClubs : list[dict]
            Clubs this user has joined.
            Item fields:
            - clubName: club display name
            - slug: club unique slug
            - urlLogo: club logo URL
        profileProtected : bool
            Whether profile visibility/privacy protection is enabled.
        """

        access_token = get_access_token()

        print("TOKEN MCP:", access_token)
        response_json = api.get_account(access_token=access_token)

        if isinstance(response_json, dict):
            return response_json.get("data")

        return response_json

    @mcp.tool()
    def get_my_player_rating():
        """
        Get the authenticated user's badminton skill rating profile.

        Endpoint
        --------
        GET /player-rating

        Returns
        -------
        A player rating object with these fields:
        - id: rating record id
        - experience: experience score
        - serve: serve score
        - smash: smash score
        - clear: clear score
        - dropShot: drop shot score
        - drive: drive score
        - netShot: net shot score
        - doubles: doubles play score
        - defense: defense score
        - footwork: footwork score
        - stamina: stamina score
        - tactics: tactics score
        - averageTechnicalScore: average technical score
        - overallScore: overall rating score
        - skillLevel: calculated skill level
        - slug: player slug
        - verifyCount: number of verifications
        """

        access_token = get_access_token()

        return api.get_player_rating(access_token=access_token)

    @mcp.tool()
    def get_my_schedule():
        """
        Get the authenticated user's schedule with pagination.

        Endpoint
        --------
        GET /schedule

        Parameters
        ----------
        page : int
            Zero-based page index. Default is 0.

        size : int
            Number of schedule items per page. Default is 20.

        Returns
        -------
        A paged response of schedule items. Each item contains:
        - id: schedule id
        - name: schedule name
        - startTime: start datetime (ISO-8601)
        - endTime: end datetime (ISO-8601)
        - status: schedule status enum
        - createdAt: creation timestamp
        - slug: related slug
        """

        access_token = get_access_token()

        return api.get_schedule(
            access_token=access_token,
            page=0,
            size=5,
        )

def find_user_nearby_tools(mcp):    
    @mcp.tool()
    def get_nearby_badminton_players(
    ):
        """
        Lấy danh sách các người chơi cầu lông ở gần vị trí của người dùng.

        Get a list of nearby badminton players based on the user's location.


        Returns
        -------
        Trả về dữ liệu phân trang chứa danh sách người chơi gần người dùng, có địa chỉ địa chỉ cụ thể

        A paginated JSON response containing a list of badminton players nearby user, and have specific address.
        """

        access_token = get_access_token()

        return api.get_nearby_badminton_players(
            access_token=access_token,  
        )
