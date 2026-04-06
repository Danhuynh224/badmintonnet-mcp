# BadmintonNet MCP Server

MCP server cho BadmintonNet, cung cấp các tool để truy vấn va tuong tac voi du lieu cau long nhu club, event, tournament, profile va tim kiem web bo tro.

Server duoc xay dung bang Python, `FastMCP`, va chay qua SSE app tren cong `3001`.

## Tinh nang

- Lay danh sach club cau long cong khai
- Tham gia club theo ten
- Tim club gan vi tri nguoi dung
- Lay danh sach club event cong khai
- Tham gia event theo ten
- Tim event gan vi tri nguoi dung
- Lay thong tin profile cua nguoi dung dang dang nhap
- Lay player rating cua nguoi dung
- Lay lich ca nhan
- Lay danh sach tournament
- Tim tournament gan vi tri nguoi dung
- Tim kiem web bang DDGS va trich xuat noi dung tu ket qua dau

## Cau truc du an

```text
.
|-- api/        # Goi toi SportsNet API
|-- auth/       # Lay header va access token tu request hien tai
|-- tools/      # Dinh nghia MCP tools
|-- config.py   # Bien moi truong va base URL
|-- server.py   # Diem vao chinh de chay MCP server
|-- requirements.txt
|-- Dockerfile
```

## Yeu cau

- Python 3.12+
- Docker (neu muon chay bang container)
- Backend SportsNet API dang hoat dong

## Cai dat local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install uvicorn
```

## Bien moi truong

Project doc 2 bien moi truong trong [`config.py`](d:/TieuLuan/badmintonnet-mcp/config.py):

- `SPORTSNET_API_URL`: URL backend API, mac dinh la `http://localhost:8080/api`
- `SPORTSNET_FE_URL`: URL frontend, mac dinh la `http://localhost:3000`

Vi du PowerShell:

```powershell
$env:SPORTSNET_API_URL="http://localhost:8080/api"
$env:SPORTSNET_FE_URL="http://localhost:3000"
```

## Chay local

```bash
python server.py
```

Server se lang nghe tai:

```text
http://0.0.0.0:3001
```

## Authentication

Server doc bearer token tu header `Authorization` cua request den SSE app va luu vao request context. Nhung tool can xac thuc se dung token nay de goi sang SportsNet API.

Format header:

```text
Authorization: Bearer <access_token>
```

Neu khong co token, mot so tool public van co the hoat dong, nhung cac tool can tai khoan nguoi dung se that bai hoac tra ve du lieu rong tuy theo backend.

## Danh sach tool

### Club

- `get_public_badminton_clubs`
- `join_club`
- `get_nearby_badminton_clubs`

### Club Event

- `get_public_club_events`
- `join_event`
- `get_nearby_club_events`

### Profile

- `get_my_profile_data`
- `get_my_player_rating`
- `get_my_schedule`
- `get_nearby_badminton_players`

### Tournament

- `get_my_club_tournaments`
- `get_nearby_badminton_tournaments`

### Web Search

- `search_and_extract_content`

## Chay voi Docker

Build image:

```bash
docker build -t badmintonnet-mcp .
```

Run container:

```bash
docker run --rm -p 3001:3001 ^
  -e SPORTSNET_API_URL=http://host.docker.internal:8080/api ^
  -e SPORTSNET_FE_URL=http://host.docker.internal:3000 ^
  badmintonnet-mcp
```

Neu ban chay tren Linux, co the can thay `host.docker.internal` bang IP hoac ten host phu hop.

## Cong nghe su dung

- Python
- FastMCP
- Uvicorn
- Requests
- DDGS
- Starlette

## Ghi chu

- Hien tai project chay qua SSE app cua MCP.
- `uvicorn` dang duoc cai truc tiep trong Dockerfile va can cai them khi chay local.
- Repo co `.dockerignore` de tranh copy `venv`, `.git`, cache va `.env` vao image.
