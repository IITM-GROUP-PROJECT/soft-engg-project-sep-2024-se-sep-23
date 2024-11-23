import pytest
import requests
import json

BASE = "http://127.0.0.1:5000"
access_token_inst = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjI3Mjg3MSwianRpIjoiMTYxNTU0ODgtMTA5Ni00YmY3LTkzMTItMjM0YjViZjJlNmUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im5ld2luc3RydWN0b3JAaWl0bS5hYy5pbiIsIm5iZiI6MTczMjI3Mjg3MSwiY3NyZiI6ImY0ZDMxMmFjLWZhNTItNGRiMC04MmYyLTlmZDdiMWI5MzNlYiIsImV4cCI6MTczMjI3Mzc3MX0.jD1cMVG_Q7mQSsItgBmpOuy6pECjMsyaWOHngAOZuw4"

# Test cases for /api/ai_eval/{student_project_id} (POST)
def test_ai_evaluation_post():
    student_project_id = 1  # Replace with a valid student project ID
    url = BASE + f"/api/ai_eval/{student_project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}', 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for project report not found
    student_project_id = 9999  # Replace with an invalid student project ID
    url = BASE + f"/api/ai_eval/{student_project_id}"
    response = requests.post(url, headers=headers)
    expected_status_code = 400
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for unauthorized access
    headers = {'Authorization': 'Bearer Invalid-Token', 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    expected_status_code = 401
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

# Test cases for /api/ai_eval/{student_project_id} (GET)
def test_ai_evaluation_get():
    student_project_id = 1  # Replace with a valid student project ID
    url = BASE + f"/api/ai_eval/{student_project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for evaluation not found
    student_project_id = 9999  # Replace with an invalid student project ID
    url = BASE + f"/api/ai_eval/{student_project_id}"
    response = requests.get(url, headers=headers)
    expected_status_code = 404
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for unauthorized access
    headers = {'Authorization': 'Bearer Invalid-Token'}
    response = requests.get(url, headers=headers)
    expected_status_code = 401
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

if __name__ == "__main__":
    pytest.main()