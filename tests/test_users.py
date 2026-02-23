import pytest
from jose import jwt
from app import schemas
from app.config import settings

# ==========================================
# INCORRECT LOGIN / VALIDATION CASES (403, 422)
# ==========================================

@pytest.mark.parametrize("email, password, status_code", [
    (None, "6789", 422),
    ("uarbeingwatched@gmail.com", None, 422),
    ("uarbeingwatched@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "6789", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code

# ==========================================
# SUCCESS CASES (201, 200)
# ==========================================

def test_create_user(client):
    res = client.post("/users/", json={"email": "uarbeingwatched@gmail.com", "password": "6789"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "uarbeingwatched@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login/", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200