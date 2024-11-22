import pytest
import requests
import json

BASE = "http://127.0.0.1:5000"

def test_instructor_signup_and_login():
    # Instructor Signup
    signup_url = BASE + "/api/instructor_signup"
    signup_data = {"email": "newinstructor@iitm.ac.in", "password": "pass12345567"}
    signup_headers = {'Content-Type': 'application/json'}
    signup_response = requests.post(signup_url, data=json.dumps(signup_data), headers=signup_headers)
    
    # Expected outcome for signup
    expected_signup_status_code = 200
    expected_signup_message = "Registered successfully"
    
    # Actual output for signup
    actual_signup_status_code = signup_response.status_code
    actual_signup_response = signup_response.json()
    
    # Result for signup
    assert actual_signup_status_code == expected_signup_status_code, f"Expected {expected_signup_status_code}, got {actual_signup_status_code}"
    assert actual_signup_response['message'] == expected_signup_message, f"Expected message '{expected_signup_message}', got '{actual_signup_response['message']}'"
    
    # Instructor Login
    login_url = BASE + "/api/instructor_login"
    login_data = {"email": "newinstructor@iitm.ac.in", "password": "pass12345567"}
    login_headers = {'Content-Type': 'application/json'}
    login_response = requests.post(login_url, data=json.dumps(login_data), headers=login_headers)
    
    # Expected outcome for login
    expected_login_status_code = 200
    expected_login_keys = ['access_token']
    
    # Actual output for login
    actual_login_status_code = login_response.status_code
    actual_login_response = login_response.json()
    
    # Result for login
    assert actual_login_status_code == expected_login_status_code, f"Expected {expected_login_status_code}, got {actual_login_status_code}"
    assert all(key in actual_login_response for key in expected_login_keys), f"Expected keys {expected_login_keys}, got {actual_login_response.keys()}"

def test_student_signup_and_login():
    # Student Signup
    signup_url = BASE + "/api/student_signup"
    signup_data = {"email": "abcd@iitm.ac.in", "password": "test1234", "github_username": "testuser"}
    signup_headers = {'Content-Type': 'application/json'}
    signup_response = requests.post(signup_url, data=json.dumps(signup_data), headers=signup_headers)
    
    # Expected outcome for signup
    expected_signup_status_code = 200
    expected_signup_message = "Registered successfully"
    
    # Actual output for signup
    actual_signup_status_code = signup_response.status_code
    actual_signup_response = signup_response.json()
    
    # Result for signup
    assert actual_signup_status_code == expected_signup_status_code, f"Expected {expected_signup_status_code}, got {actual_signup_status_code}"
    assert actual_signup_response['message'] == expected_signup_message, f"Expected message '{expected_signup_message}', got '{actual_signup_response['message']}'"
    
    # Student Login
    login_url = BASE + "/api/student_login"
    login_data = {"email": "abcd@iitm.ac.in", "password": "test1234"}
    login_headers = {'Content-Type': 'application/json'}
    login_response = requests.post(login_url, data=json.dumps(login_data), headers=login_headers)
    
    # Expected outcome for login
    expected_login_status_code = 200
    expected_login_keys = ['access_token']
    
    # Actual output for login
    actual_login_status_code = login_response.status_code
    actual_login_response = login_response.json()
    
    # Result for login
    assert actual_login_status_code == expected_login_status_code, f"Expected {expected_login_status_code}, got {actual_login_status_code}"
    assert all(key in actual_login_response for key in expected_login_keys), f"Expected keys {expected_login_keys}, got {actual_login_response.keys()}"

def test_instructor_login_failure():
    url = BASE + "/api/instructor_login"
    data = {"email": "wrongemail@iitm.ac.in", "password": "wrongpassword"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 401
    expected_message = "Invalid email or password"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

def test_student_login_failure():
    url = BASE + "/api/student_login"
    data = {"email": "wrongemail@iitm.ac.in", "password": "wrongpassword"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 401
    expected_message = "Invalid email or password"
    
    # Actual output
    actual_status_code = response.status_code
    actual_response = response.json()
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"
    assert actual_response['message'] == expected_message, f"Expected message '{expected_message}', got '{actual_response['message']}'"

if __name__ == "__main__":
    pytest.main()