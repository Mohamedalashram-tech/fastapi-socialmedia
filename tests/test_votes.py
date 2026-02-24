import pytest
from app import schemas

# ==========================================
# UNAUTHORIZED CASES (401)
# ==========================================

def test_unauthorized_user_vote_on_post(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401

# ==========================================
# ERROR & CONFLICT CASES (404, 409)
# ==========================================

def test_vote_on_non_exist_post(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 9999, "dir": 1})
    assert res.status_code == 404

def test_delete_non_exist_vote(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id, "dir": 0})
    assert res.status_code == 404

def test_vote_twice_on_post(authorized_client, test_posts, test_vote, test_user):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

# ==========================================
# SUCCESS CASES (201) - النظام الجديد
# ==========================================

def test_vote_like_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201
    assert res.json()["message"] == "Successfully added LIKE"

def test_vote_dislike_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": -1})
    assert res.status_code == 201
    assert res.json()["message"] == "Successfully added DISLIKE"

def test_change_vote_from_like_to_dislike(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": -1})
    assert res.status_code == 201
    assert res.json()["message"] == "Successfully changed vote to DISLIKE"

def test_remove_vote_successfully(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201
    assert res.json()["message"] == "Successfully removed vote"