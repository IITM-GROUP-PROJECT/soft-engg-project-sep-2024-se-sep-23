
import pytest
import requests
import json

BASE = "http://127.0.0.1:5000"
access_token_inst = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjI3Mjg3MSwianRpIjoiMTYxNTU0ODgtMTA5Ni00YmY3LTkzMTItMjM0YjViZjJlNmUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im5ld2luc3RydWN0b3JAaWl0bS5hYy5pbiIsIm5iZiI6MTczMjI3Mjg3MSwiY3NyZiI6ImY0ZDMxMmFjLWZhNTItNGRiMC04MmYyLTlmZDdiMWI5MzNlYiIsImV4cCI6MTczMjI3Mzc3MX0.jD1cMVG_Q7mQSsItgBmpOuy6pECjMsyaWOHngAOZuw4"

def test_edit_project_get_success():
    project_id = 1
    url = f"{BASE}/api/edit_project/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert 'title' in actual_response, f"Expected 'title' in response, got {actual_response.keys()}"

def test_edit_project_get_unauthorized():
    project_id = 1
    url = f"{BASE}/api/edit_project/{project_id}"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_edit_project_get_not_found():
    project_id = 999  # Assuming this project ID does not exist
    url = f"{BASE}/api/edit_project/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 404
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_edit_project_put_success():
    project_id = 1
    url = f"{BASE}/api/edit_project/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}', 'Content-Type': 'application/json'}
    data = {
        "title": "Updated Project Title",
        "problem": "Updated Problem Statement",
        "milestones": [{"title": "Milestone 1", "description": "Description 1", "deadline": "2024-12-31"}],
        "student_ids": [1, 2]
    }
    response = requests.put(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    expected_message = "Project updated successfully"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_edit_project_put_missing_fields():
    project_id = 1
    url = f"{BASE}/api/edit_project/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}', 'Content-Type': 'application/json'}
    data = {
        "title": "Updated Project Title"
    }
    response = requests.put(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 400
    expected_message = "Missing required field: problem"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_edit_project_put_unauthorized():
    project_id = 1
    url = f"{BASE}/api/edit_project/{project_id}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "title": "Updated Project Title",
        "problem": "Updated Problem Statement",
        "milestones": [{"title": "Milestone 1", "description": "Description 1", "deadline": "2024-12-31"}],
        "student_ids": [1, 2]
    }
    response = requests.put(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_edit_project_put_not_found():
    project_id = 999  # Assuming this project ID does not exist
    url = f"{BASE}/api/edit_project/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}', 'Content-Type': 'application/json'}
    data = {
        "title": "Updated Project Title",
        "problem": "Updated Problem Statement",
        "milestones": [{"title": "Milestone 1", "description": "Description 1", "deadline": "2024-12-31"}],
        "student_ids": [1, 2]
    }
    response = requests.put(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 404
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_delete_project_success():
    project_id = 1
    url = f"{BASE}/api/delete_project/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.delete(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    expected_message = "Project deleted successfully"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_delete_project_unauthorized():
    project_id = 1
    url = f"{BASE}/api/delete_project/{project_id}"
    response = requests.delete(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_delete_project_not_found():
    project_id = 999  # Assuming this project ID does not exist
    url = f"{BASE}/api/delete_project/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.delete(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 404
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

if __name__ == "__main__":
    pytest.main()