import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.insert(0, project_root)

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_comment_flow():
    # Reset database using subprocess directly
    import subprocess

    try:
        subprocess.run(["python", "scripts/setup_db.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to reset database")
        return False

    print("\nTesting Comment Management Flow:")

    # 1. Register and login
    register_data = {
        "email": "commenter5@example.com",
        "password": "secret123",
        "full_name": "Test Commenter",
    }
    response = client.post("/api/v1/auth/register", json=register_data)
    if response.status_code != 200:
        print("❌ Registration failed:", response.json())
        return False
    print("✅ User registered successfully")

    # Login to get token
    login_data = {"email": "commenter5@example.com", "password": "secret123"}
    response = client.post("/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        print("❌ Login failed:", response.json())
        return False
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")

    # 2. Create an article first
    article_data = {
        "title": "Test Article for Comments",
        "content": "This is a test article content.",
        "summary": "Testing comments",
        "tags": ["test"],
        "status": "published",
    }
    response = client.post("/api/v1/articles", json=article_data, headers=headers)
    if response.status_code != 200:
        print("❌ Article creation failed:", response.json())
        return False
    article_id = response.json()["id"]
    print("✅ Article created successfully")

    # 3. Create a comment
    comment_data = {
        "content": "This is a test comment",
        "article_id": article_id,
    }
    response = client.post("/api/v1/comments", json=comment_data, headers=headers)
    if response.status_code != 200:
        print("❌ Comment creation failed:", response.json())
        return False
    comment_id = response.json()["id"]
    print("✅ Comment created successfully")

    # 4. List article comments
    response = client.get(f"/api/v1/comments/article/{article_id}")
    if response.status_code != 200:
        print("❌ Comment listing failed:", response.json())
        return False
    print("✅ Comments listed successfully")

    # 5. Update comment
    update_data = {"content": "Updated comment content"}
    response = client.patch(
        f"/api/v1/comments/{comment_id}", json=update_data, headers=headers
    )
    if response.status_code != 200:
        print("❌ Comment update failed:", response.json())
        return False
    print("✅ Comment updated successfully")

    # 6. Delete comment
    response = client.delete(f"/api/v1/comments/{comment_id}", headers=headers)
    if response.status_code != 200:
        print("❌ Comment deletion failed:", response.json())
        return False
    print("✅ Comment deleted successfully")

    # Test pagination
    # Create multiple comments
    for i in range(15):
        comment_data = {
            "content": f"Test comment {i}",
            "article_id": article_id,
        }
        response = client.post("/api/v1/comments", json=comment_data, headers=headers)
        if response.status_code != 200:
            print("❌ Comment creation failed:", response.json())
            return False

    # Test first page
    response = client.get(f"/api/v1/comments/article/{article_id}?page=1&size=10")
    if response.status_code != 200:
        print("❌ Comment listing failed:", response.json())
        return False
    data = response.json()
    if len(data["items"]) != 10 or data["total"] < 15:
        print("❌ Comment pagination incorrect")
        return False
    print("✅ Comment pagination working correctly")

    # Create a comment for testing permissions
    comment_data = {
        "content": "Comment for permission test",
        "article_id": article_id,
    }
    response = client.post("/api/v1/comments", json=comment_data, headers=headers)
    if response.status_code != 200:
        print("❌ Comment creation failed:", response.json())
        return False
    permission_test_comment_id = response.json()["id"]

    # Test error handling
    # 1. Try to update non-existent comment
    response = client.patch(
        "/api/v1/comments/99999",
        json={"content": "Updated content"},
        headers=headers,
    )
    if response.status_code != 404:
        print("❌ Non-existent comment error handling failed")
        return False
    print("✅ Non-existent comment error handled correctly")

    # 2. Try to update someone else's comment
    # First create another user
    register_data = {
        "email": "other@example.com",
        "password": "secret123",
        "full_name": "Other User",
    }
    response = client.post("/api/v1/auth/register", json=register_data)
    if response.status_code != 200:
        print("❌ Other user registration failed:", response.json())
        return False

    # Login as other user
    login_data = {"email": "other@example.com", "password": "secret123"}
    response = client.post("/api/v1/auth/login", json=login_data)
    other_token = response.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    # Try to update first user's comment
    response = client.patch(
        f"/api/v1/comments/{permission_test_comment_id}",
        json={"content": "Malicious update"},
        headers=other_headers,
    )
    if response.status_code != 403:
        print("❌ Permission error handling failed")
        return False
    print("✅ Permission error handled correctly")

    return True


if __name__ == "__main__":
    success = test_comment_flow()
    print("\n🔍 Final Result:", "Success! ✨" if success else "Failed ❌")
