import pytest
import requests
import json

BASE = "http://127.0.0.1:5000"
instructor_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjI3Mjg3MSwianRpIjoiMTYxNTU0ODgtMTA5Ni00YmY3LTkzMTItMjM0YjViZjJlNmUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im5ld2luc3RydWN0b3JAaWl0bS5hYy5pbiIsIm5iZiI6MTczMjI3Mjg3MSwiY3NyZiI6ImY0ZDMxMmFjLWZhNTItNGRiMC04MmYyLTlmZDdiMWI5MzNlYiIsImV4cCI6MTczMjI3Mzc3MX0.jD1cMVG_Q7mQSsItgBmpOuy6pECjMsyaWOHngAOZuw4"

# Test cases for /api/get-commit-data (GET)
def test_get_commit_data():
    student_project_id = 1  # Replace with a valid student project ID
    url = BASE + "/api/get-commit-data"
    headers = {'Authorization': f'Bearer {instructor_token}'}
    params = {'student_project_id': student_project_id}
    response = requests.get(url, headers=headers, params=params)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for missing student_project_id
    response = requests.get(url, headers=headers)
    expected_status_code = 400
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for unauthorized access
    headers = {'Authorization': 'Bearer Invalid-Token'}
    response = requests.get(url, headers=headers, params=params)
    expected_status_code = 401
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

# Test cases for /api/fetch-commits (POST)
def test_fetch_commits():
    url = BASE + "/api/fetch-commits"
    headers = {'Authorization': f'Bearer {instructor_token}', 'Content-Type': 'application/json'}
    data = {
        "owner": "octocat",
        "repo": "Hello-World",
        "student_project_id": 1  # Replace with a valid student project ID
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for missing fields
    data = {"owner": "octocat", "repo": "Hello-World"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    expected_status_code = 400
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for unauthorized access
    headers = {'Authorization': 'Bearer Invalid-Token', 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    expected_status_code = 401
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for no commits found
    data = {
        "owner": "octocat",
        "repo": "Empty-Repo",  # Replace with a repo that has no commits
        "student_project_id": 1
    }
    headers = {'Authorization': f'Bearer {instructor_token}', 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    expected_status_code = 409
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

if __name__ == "__main__":
    pytest.main()