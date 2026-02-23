import pytest

# ==========================================
# UNAUTHORIZED CASES (401)
# ==========================================

def test_unauthorized_user_vote_on_post(client, test_user, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401

# ==========================================
# ERROR & CONFLICT CASES (404, 409)
# ==========================================

def test_vote_on_non_exist_post(authorized_client, test_posts, test_user):
    res = authorized_client.post("/vote/", json={"post_id": 9999, "dir": 1})
    assert res.status_code == 404

def test_delete_non_exist_vote(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id, "dir": 0})
    assert res.status_code == 404

def test_vote_twice_on_post(authorized_client, test_posts, test_vote, test_user):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409
    assert res.json()["detail"] == f'user {test_user["id"]} has already voted on  the post with id {test_posts[3].id}'

# ==========================================
# SUCCESS CASES (201)
# ==========================================

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201