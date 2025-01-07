import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.insert(0, project_root)

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_profile_flow():
    # Reset database using subprocess directly
    import subprocess

    try:
        subprocess.run(["python", "scripts/setup_db.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to reset database")
        return False

    print("\nTesting User Profile Flow:")

    # 1. Register and login
    register_data = {
        "email": "profile_test3@example.com",
        "password": "secret123",
        "full_name": "Profile Tester",
    }
    response = client.post("/api/v1/auth/register", json=register_data)
    if response.status_code != 200:
        print("❌ Registration failed:", response.json())
        return False
    print("✅ User registered successfully")

    # Login to get token
    login_data = {"email": "profile_test3@example.com", "password": "secret123"}
    response = client.post("/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        print("❌ Login failed:", response.json())
        return False
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")

    # 2. Get own profile
    response = client.get("/api/v1/users/me", headers=headers)
    if response.status_code != 200:
        print("❌ Profile retrieval failed:", response.json())
        return False
    user_id = response.json()["id"]
    print("✅ Profile retrieved successfully")

    # 3. Update profile
    update_data = {
        "bio": "I am a test user",
        "avatar_url": "https://example.com/avatar.jpg",
    }
    response = client.patch("/api/v1/users/me", json=update_data, headers=headers)
    if response.status_code != 200:
        print("❌ Profile update failed:", response.json())
        return False
    print("✅ Profile updated successfully")

    # 4. Get detailed profile with activity
    response = client.get(f"/api/v1/users/{user_id}")
    if response.status_code != 200:
        print("❌ Detailed profile retrieval failed:", response.json())
        return False
    profile = response.json()
    if "recent_articles" not in profile or "recent_comments" not in profile:
        print("❌ Profile activity missing")
        return False
    print("✅ Detailed profile retrieved successfully")

    # Test error handling
    # 1. Try to get non-existent user profile
    response = client.get("/api/v1/users/99999")
    if response.status_code != 404:
        print("❌ Non-existent user error handling failed")
        return False
    print("✅ Non-existent user error handled correctly")

    # 2. Try to update profile without authentication
    response = client.patch(
        "/api/v1/users/me",
        json={"bio": "Unauthorized update"},
    )
    if response.status_code != 401:
        print("❌ Unauthorized error handling failed")
        return False
    print("✅ Unauthorized error handled correctly")

    return True


if __name__ == "__main__":
    success = test_profile_flow()
    print("\n🔍 Final Result:", "Success! ✨" if success else "Failed ❌")
