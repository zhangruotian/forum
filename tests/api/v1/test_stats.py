import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.insert(0, project_root)

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_stats_flow():
    # Reset database using subprocess directly
    import subprocess

    try:
        subprocess.run(["python", "scripts/setup_db.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to reset database")
        return False

    print("\nTesting User and Article Stats:")

    # 1. Register and login
    register_data = {
        "email": "stats_test@example.com",
        "password": "secret123",
        "full_name": "Stats Tester",
    }
    response = client.post("/api/v1/auth/register", json=register_data)
    if response.status_code != 200:
        print("❌ Registration failed:", response.json())
        return False
    print("✅ User registered successfully")

    # Login to get token
    login_data = {"email": "stats_test@example.com", "password": "secret123"}
    response = client.post("/api/v1/auth/login", json=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")

    # 2. Create article and check stats
    article_data = {
        "title": "Test Article",
        "content": "Content",
        "tags": ["test"],
        "status": "published",
    }
    response = client.post("/api/v1/articles", json=article_data, headers=headers)
    article_id = response.json()["id"]

    # Check user's article count
    response = client.get("/api/v1/users/me", headers=headers)
    if response.json()["article_count"] != 1:
        print("❌ Article count not updated")
        return False
    print("✅ Article count updated successfully")

    # Test comment stats
    comment_data = {"content": "Test comment", "article_id": article_id}
    response = client.post("/api/v1/comments", json=comment_data, headers=headers)

    # Check user's comment count
    response = client.get("/api/v1/users/me", headers=headers)
    if response.json()["comment_count"] != 1:
        print("❌ Comment count not updated")
        return False
    print("✅ Comment count updated successfully")

    # Check article's comment count
    response = client.get(f"/api/v1/articles/{article_id}")
    if response.json()["comment_count"] != 1:
        print("❌ Article comment count not updated")
        return False
    print("✅ Article comment count updated successfully")

    return True


if __name__ == "__main__":
    success = test_stats_flow()
    print("\n🔍 Final Result:", "Success! ✨" if success else "Failed ❌")
