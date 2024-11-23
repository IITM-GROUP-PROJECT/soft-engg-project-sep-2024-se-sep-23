import pytest
import requests
import json

BASE = "http://127.0.0.1:5000"
access_token_inst = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjI3Mjg3MSwianRpIjoiMTYxNTU0ODgtMTA5Ni00YmY3LTkzMTItMjM0YjViZjJlNmUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im5ld2luc3RydWN0b3JAaWl0bS5hYy5pbiIsIm5iZiI6MTczMjI3Mjg3MSwiY3NyZiI6ImY0ZDMxMmFjLWZhNTItNGRiMC04MmYyLTlmZDdiMWI5MzNlYiIsImV4cCI6MTczMjI3Mzc3MX0.jD1cMVG_Q7mQSsItgBmpOuy6pECjMsyaWOHngAOZuw4"

def test_instructor_dashboard_success():
    url = f"{BASE}/api/instructor_dashboard"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert 'projects' in actual_response, f"Expected 'projects' in response, got {actual_response.keys()}"

def test_instructor_dashboard_unauthorized():
    url = f"{BASE}/api/instructor_dashboard"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_project_details_success():
    project_id = 1
    url = f"{BASE}/api/project_details/{project_id}"
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

def test_project_details_unauthorized():
    project_id = 1
    url = f"{BASE}/api/project_details/{project_id}"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_project_details_not_found():
    project_id = 999  # Assuming this project ID does not exist
    url = f"{BASE}/api/project_details/{project_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 404
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_track_progress_success():
    project_id = 1
    student_id = 1
    url = f"{BASE}/api/track_progress/{project_id}/{student_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert 'progress' in actual_response, f"Expected 'progress' in response, got {actual_response.keys()}"

def test_track_progress_unauthorized():
    project_id = 1
    student_id = 1
    url = f"{BASE}/api/track_progress/{project_id}/{student_id}"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_track_progress_not_found():
    project_id = 999  # Assuming this project ID does not exist
    student_id = 999  # Assuming this student ID does not exist
    url = f"{BASE}/api/track_progress/{project_id}/{student_id}"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 404
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

if __name__ == "__main__":
    pytest.main()