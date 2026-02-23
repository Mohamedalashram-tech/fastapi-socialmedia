import pytest
from app import schemas

# ==========================================
# UNAUTHORIZED CASES (401)
# ==========================================

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "title", "content": "content", "published": True})
    assert res.status_code == 401

def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {"title": "updated_title", "content": "updated_content", "id": test_posts[0].id}
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

# ==========================================
# NOT FOUND (404) & FORBIDDEN (403) CASES
# ==========================================

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/4444")
    assert res.status_code == 404

def test_delete_non_existed_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete("/posts/9999")
    assert res.status_code == 404

def test_update_non_existed_post(authorized_client, test_posts, test_user):
    data = {"title": "updated_title", "content": "updated_content", "id": test_posts[0].id}
    res = authorized_client.put("/posts/9999", json=data)
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_other_user_post(authorized_client, test_posts, test_user):
    data = {"title": "updated_title", "content": "updated_content", "id": test_posts[3].id}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

# ==========================================
# SUCCESS CASES (200, 201, 204)
# ==========================================

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("title_1", "content_1", True),
    ("I do love chess", "Sac the rooook", True),
    ("title_3", "content_3", False),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.CreatePost(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

def test_update_post(authorized_client, test_posts, test_user):
    data = {"title": "updated_title", "content": "updated_content", "id": test_posts[0].id}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_delete_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204