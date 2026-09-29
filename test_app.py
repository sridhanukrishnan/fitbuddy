import os
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_user, get_original_plan, SessionLocal, User, WorkoutPlan

client = TestClient(app)

def run_tests():
    print("=== 1. Testing GET / (Home Page) ===")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "FitBuddy" in res.text
    assert "Generate Plan" in res.text
    print("PASS: Home page rendered correctly.")

    print("\n=== 2. Testing POST /generate-workout (Form submission) ===")
    form_data = {
        "username": "Alex Rivers",
        "user_id": 101,
        "age": 28,
        "weight": 75.5,
        "goal": "Muscle Gain and Fat Loss",
        "intensity": "High"
    }
    res = client.post("/generate-workout", data=form_data)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "Alex Rivers" in res.text
    assert "#101" in res.text
    assert "Muscle Gain and Fat Loss" in res.text
    assert "Day 1:" in res.text or "Workout Plan" in res.text
    assert "Nutrition Tip" in res.text
    print("PASS: Workout generated and rendered on result page.")

    # Verify database state
    user = get_user(101)
    assert user is not None
    assert user.name == "Alex Rivers"
    original_plan = get_original_plan(101)
    assert original_plan is not None
    print(f"PASS: User and Plan persisted in SQLite: {user.name} (ID: {user.id})")

    print("\n=== 3. Testing POST /submit-feedback (Plan update) ===")
    feedback_data = {
        "user_id": 101,
        "feedback": "Include more core exercises and 20 mins cardio"
    }
    res = client.post("/submit-feedback", data=feedback_data)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "Your plan has been updated based on your feedback!" in res.text
    assert "Updated Workout Plan" in res.text
    print("PASS: Feedback received, updated plan generated and rendered.")

    print("\n=== 4. Testing GET /view-all-users (Admin Dashboard) ===")
    res = client.get("/view-all-users")
    assert res.status_code == 200
    assert "FitBuddy - All Users & Workout Plans" in res.text
    assert "Alex Rivers" in res.text
    assert "#101" in res.text
    print("PASS: Admin dashboard displays user records and plans.")

    print("\n=== 5. Testing REST API: POST /generate-workout/gemini ===")
    api_res = client.post("/generate-workout/gemini", json={"goal": "Weight Loss", "intensity": "Medium"})
    assert api_res.status_code == 200
    data = api_res.json()
    assert data["model"] == "gemini-pro"
    assert "workout_plan" in data
    print("PASS: /generate-workout/gemini API works.")

    print("\n=== 6. Testing REST API: GET /nutrition-tip ===")
    tip_res = client.get("/nutrition-tip?goal=muscle%20gain")
    assert tip_res.status_code == 200
    tip_data = tip_res.json()
    assert "nutrition_tip" in tip_data
    assert len(tip_data["nutrition_tip"]) > 10
    print("PASS: /nutrition-tip API works.")

    print("\n=== 7. Testing REST API: POST /generate-plan ===")
    gen_plan_res = client.post("/generate-plan", json={
        "username": "Sarah Connor",
        "user_id": 202,
        "age": 32,
        "weight": 62.0,
        "goal": "Endurance and Core Strength",
        "intensity": "High"
    })
    assert gen_plan_res.status_code == 200
    print("PASS: /generate-plan API created user and plan.")

    print("\n=== 8. Testing REST API: POST /update-plan/{user_id} ===")
    update_res = client.post("/update-plan/202", json={"feedback": "Add more stretching"})
    assert update_res.status_code == 200
    assert "updated_plan" in update_res.json()
    print("PASS: /update-plan/{user_id} updated plan via API.")

    print("\n=== 9. Testing REST API: GET /api/users ===")
    users_res = client.get("/api/users")
    assert users_res.status_code == 200
    users_data = users_res.json()
    assert users_data["total_users"] >= 2
    print(f"PASS: /api/users returned {users_data['total_users']} users.")

    print("\n=== 10. Testing Admin Delete User ===")
    del_res = client.post("/delete-user/202", follow_redirects=True)
    assert del_res.status_code == 200
    assert get_user(202) is None
    print("PASS: User #202 deleted successfully.")

    print("\nALL 10 TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
