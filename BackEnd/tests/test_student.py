
import pytest
import requests
import json

BASE = "http://127.0.0.1:5000"
access_token_student = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjMyOTczMywianRpIjoiODczNDVkNDMtYmQ0YS00YzhkLTgyMjAtYjI2NDQzZmRkMGY1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3RzdHVkZW50QGlpdG0uYWMuaW4iLCJuYmYiOjE3MzIzMjk3MzMsImNzcmYiOiI2NTZjZmQ2MC04ZjY3LTRjZTktOTliNS0xNmRjNDFlMTFhOWEiLCJleHAiOjE3MzIzMzI3MzN9.Iax6mt8W2_gwrIkf7pK_LmoTTOmKz9toyXG9fowQ-e0"

def test_student_dashboard_success():
    url = f"{BASE}/api/student_dashboard"
    headers = {'Authorization': f'Bearer {access_token_student}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert isinstance(actual_response, list), f"Expected list, got {type(actual_response)}"

def test_student_dashboard_unauthorized():
    url = f"{BASE}/api/student_dashboard"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_project_info_get_success():
    project_id = 1
    url = f"{BASE}/api/project_info/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_student}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert 'title' in actual_response, f"Expected 'title' in response, got {actual_response.keys()}"

def test_project_info_get_unauthorized():
    project_id = 1
    url = f"{BASE}/api/project_info/{project_id}"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_project_info_get_not_found():
    project_id = 999  # Assuming this project ID does not exist
    url = f"{BASE}/api/project_info/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_student}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 404
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_project_info_post_success():
    project_id = 1
    url = f"{BASE}/api/project_info/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_student}', 'Content-Type': 'application/json'}
    data = {
        "milestones": [
            {"id": 1, "status": "Completed"},
            {"id": 2, "status": "Pending"}
        ],
        "project_report": "This is the project report."
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    expected_message = "Project info updated successfully"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_project_info_post_missing_fields():
    project_id = 1
    url = f"{BASE}/api/project_info/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_student}', 'Content-Type': 'application/json'}
    data = {
        "project_report": "This is the project report."
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 400
    expected_message = "Missing milestones data"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_project_info_post_invalid_milestones():
    project_id = 1
    url = f"{BASE}/api/project_info/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_student}', 'Content-Type': 'application/json'}
    data = {
        "milestones": "invalid_milestones_data",
        "project_report": "This is the project report."
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 400
    expected_message = "Milestones must be a list"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_project_info_post_unauthorized():
    project_id = 1
    url = f"{BASE}/api/project_info/{project_id}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "milestones": [
            {"id": 1, "status": "Completed"},
            {"id": 2, "status": "Pending"}
        ],
        "project_report": "This is the project report."
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_project_info_post_not_found():
    project_id = 999  # Assuming this project ID does not exist
    url = f"{BASE}/api/project_info/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_student}', 'Content-Type': 'application/json'}
    data = {
        "milestones": [
            {"id": 1, "status": "Completed"},
            {"id": 2, "status": "Pending"}
        ],
        "project_report": "This is the project report."
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 404
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

if __name__ == "__main__":
    pytest.main()