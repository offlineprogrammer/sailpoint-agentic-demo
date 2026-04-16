from langchain.tools import tool
import json, datetime

USERS_DB = {
    "sarah.chen": {"role": "senior_engineer", "dept": "engineering", "risk_score": 2},
    "john.doe": {"role": "engineer", "dept": "engineering", "risk_score": 7},
}
ACCESS_DB = {
    "john.doe": [
        {"resource": "finance_db", "last_reviewed": "2024-07-20", "risk": "high"},
        {"resource": "github_org", "last_reviewed": "2025-01-10", "risk": "low"},
    ]
}

@tool
def get_user_profile(user_id: str) -> str:
    """Get role, department, and risk score for a user."""
    user = USERS_DB.get(user_id)
    if not user: return json.dumps({"error": f"User {user_id} not found"})
    return json.dumps({"user_id": user_id, **user})

@tool
def check_user_access(user_id: str) -> str:
    """Return all access entitlements for a user with review dates."""
    if user_id not in ACCESS_DB:
        return json.dumps({"user": user_id, "entitlements": []})
    days_since = (datetime.date.today() -
                  datetime.date.fromisoformat(ACCESS_DB[user_id][0]["last_reviewed"])).days
    return json.dumps({
        "user": user_id,
        "entitlements": ACCESS_DB[user_id],
        "days_since_review": days_since,
        "requires_review": days_since > 90
    }, indent=2)
