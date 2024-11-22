import pytest
import requests
import json

access_token_inst = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMjI3Mjg3MSwianRpIjoiMTYxNTU0ODgtMTA5Ni00YmY3LTkzMTItMjM0YjViZjJlNmUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im5ld2luc3RydWN0b3JAaWl0bS5hYy5pbiIsIm5iZiI6MTczMjI3Mjg3MSwiY3NyZiI6ImY0ZDMxMmFjLWZhNTItNGRiMC04MmYyLTlmZDdiMWI5MzNlYiIsImV4cCI6MTczMjI3Mzc3MX0.jD1cMVG_Q7mQSsItgBmpOuy6pECjMsyaWOHngAOZuw4"


BASE = "http://127.0.0.1:5000"
def test_get_students():

    url = BASE + "/api/students"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)# Expected outcome
    de = 200
    # Expected outcome
    expected_status_code = 200# Actual output
    ode = response.status_code
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert isinstance(actual_response, list), f"Expected list, got {type(actual_response)}"

def test_get_students_unauthorized():
    url = BASE + "/api/students"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_get_courses():
    url = BASE + "/api/courses"
    headers = {'Authorization': f'Bearer {access_token_inst}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert isinstance(actual_response, list), f"Expected list, got {type(actual_response)}"
    for course in actual_response:
        assert 'id' in course and 'name' in course, f"Expected keys 'id' and 'name' in course, got {course.keys()}"

def test_get_courses_unauthorized():
    url = BASE + "/api/courses"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

def test_create_project_success():
    url = BASE + "/api/create_project"
    headers = {'Authorization': f'Bearer {access_token_inst}', 'Content-Type': 'application/json'}
    data = {
        "title": "New Project",
        "description": "Project Description",
        "course_id": 1,
        "student_ids": [1, 2]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 201
    expected_message = "Project created successfully"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_create_project_failure_missing_fields():
    url = BASE + "/api/create_project"
    headers = {'Authorization': f'Bearer {access_token_inst}', 'Content-Type': 'application/json'}
    data = {
        "title": "New Project"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 400
    expected_message = "Missing required fields"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_create_project_failure_invalid_course():
    url = BASE + "/api/create_project"
    headers = {'Authorization': f'Bearer {access_token_inst}', 'Content-Type': 'application/json'}
    data = {
        "title": "New Project",
        "description": "Project Description",
        "course_id": 999,  # Invalid course ID
        "student_ids": [1, 2]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 400
    expected_message = "Invalid course ID"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_create_project_failure_invalid_students():
    url = BASE + "/api/create_project"
    headers = {'Authorization': f'Bearer {access_token_inst}', 'Content-Type': 'application/json'}
    data = {
        "title": "New Project",
        "description": "Project Description",
        "course_id": 1,
        "student_ids": [999, 1000]  # Invalid student IDs
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 400
    expected_message = "Invalid student IDs"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_create_project_unauthorized():
    url = BASE + "/api/create_project"
    headers = {'Content-Type': 'application/json'}
    data = {
        "title": "New Project",
        "description": "Project Description",
        "course_id": 1,
        "student_ids": [1, 2]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 401
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"


    
def test_get_courses():
    url = BASE + "/api/courses"
    headers = {'Authorization': 'Bearer <access_token>'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert isinstance(actual_response, list), f"Expected list, got {type(actual_response)}"
    for course in actual_response:
        assert 'id' in course and 'name' in course, f"Expected keys 'id' and 'name' in course, got {course.keys()}"

def test_create_project_success():
    url = BASE + "/api/create_project"
    headers = {'Authorization': 'Bearer <access_token>', 'Content-Type': 'application/json'}
    data = {
        "title": "New Project",
        "description": "Project Description",
        "course_id": 1,
        "student_ids": [1, 2]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 201
    expected_message = "Project created successfully"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_create_project_failure_missing_fields():
    url = BASE + "/api/create_project"
    headers = {'Authorization': 'Bearer <access_token>', 'Content-Type': 'application/json'}
    data = {
        "title": "New Project"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 400
    expected_message = "Missing required fields"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

if __name__ == "__main__":
    pytest.main()
    

