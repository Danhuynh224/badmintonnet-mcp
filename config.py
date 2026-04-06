import os

BASE_URL = os.getenv(
    "SPORTSNET_API_URL",
    "http://localhost:8080/api"
)
FE_URL = os.getenv(
    "SPORTSNET_FE_URL",
    "http://localhost:3000"
)
