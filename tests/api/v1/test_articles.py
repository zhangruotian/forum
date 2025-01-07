import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.insert(0, project_root)

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_article_flow():
    # Reset database using subprocess directly
    import subprocess

    try:
        subprocess.run(["python", "scripts/setup_db.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to reset database")
        return False

    print("\nTesting Article Management Flow:")

    # 1. Register and login
    register_data = {
        "email": "author9@example.com",
        "password": "secret123",
        "full_name": "Test Author",
    }
    response = client.post("/api/v1/auth/register", json=register_data)
    if response.status_code != 200:
        print("❌ Registration failed:", response.json())
        return False
    print("✅ User registered successfully")

    # Login to get token
    login_data = {"email": "author9@example.com", "password": "secret123"}
    response = client.post("/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        print("❌ Login failed:", response.json())
        return False
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")

    # 2. Create article with enhanced fields
    article_data = {
        "title": "Test Article",
        "content": "This is a test article content.",
        "summary": "A brief summary of the test article",
        "tags": ["test", "example"],
        "status": "draft",
    }
    response = client.post("/api/v1/articles", json=article_data, headers=headers)
    if response.status_code != 200:
        print("❌ Article creation failed:", response.json())
        return False
    article_id = response.json()["id"]
    print("✅ Article created successfully")

    # 3. Get article
    response = client.get(f"/api/v1/articles/{article_id}")
    if response.status_code != 200:
        print("❌ Article retrieval failed:", response.json())
        return False
    print("✅ Article retrieved successfully")

    # 4. Update article
    update_data = {
        "title": "Updated Title",
        "content": "Updated content.",
    }
    response = client.patch(
        f"/api/v1/articles/{article_id}", json=update_data, headers=headers
    )
    if response.status_code != 200:
        print("❌ Article update failed:", response.json())
        return False
    print("✅ Article updated successfully")

    # 5. List articles
    response = client.get("/api/v1/articles")
    if response.status_code != 200:
        print("❌ Article listing failed:", response.json())
        return False
    print("✅ Articles listed successfully")

    # 6. Test article status update
    status_update = {"status": "published"}
    response = client.patch(
        f"/api/v1/articles/{article_id}", json=status_update, headers=headers
    )
    if response.status_code != 200:
        print("❌ Status update failed:", response.json())
        return False
    print("✅ Article status updated successfully")

    # Test pagination
    # Create multiple articles
    for i in range(15):
        article_data = {
            "title": f"Test Article {i}",
            "content": f"Content {i}",
            "tags": ["test"],
            "status": "published",
        }
        response = client.post("/api/v1/articles", json=article_data, headers=headers)
        if response.status_code != 200:
            print("❌ Article creation failed:", response.json())
            return False

    # Test first page
    response = client.get("/api/v1/articles?page=1&size=10")
    if response.status_code != 200:
        print("❌ Article listing failed:", response.json())
        return False
    data = response.json()
    if len(data["items"]) != 10 or data["total"] < 15:
        print("❌ Pagination incorrect")
        return False
    print("✅ Pagination working correctly")

    return True


if __name__ == "__main__":
    success = test_article_flow()
    print("\n🔍 Final Result:", "Success! ✨" if success else "Failed ❌")
