import pytest
import requests
import json

BASE = "http://127.0.0.1:5000"
admin_token = 'Sys-Admin-Secret'

# Test cases for /api/admin/instructors (GET)
def test_get_all_instructors():
    url = BASE + "/api/admin/instructors"
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

# Test cases for /api/admin/instructors (POST)
def test_create_instructor():
    url = BASE + "/api/admin/instructors"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {admin_token}'}
    data = {"email": "newinstructor@iitm.ac.in", "password": "password123"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 201
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for email already exists
    response = requests.post(url, data=json.dumps(data), headers=headers)
    expected_status_code = 409
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for missing fields
    data = {"email": "anotherinstructor@iitm.ac.in"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    expected_status_code = 400
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

# Test cases for /api/admin/instructors/{id} (GET)
def test_get_instructor():
    instructor_id = 1  # Replace with a valid instructor ID
    url = BASE + f"/api/admin/instructors/{instructor_id}"
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = requests.get(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for instructor not found
    instructor_id = 9999  # Replace with an invalid instructor ID
    url = BASE + f"/api/admin/instructors/{instructor_id}"
    response = requests.get(url, headers=headers)
    expected_status_code = 404
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

# Test cases for /api/admin/instructors/{id} (PUT)
def test_update_instructor():
    instructor_id = 1  # Replace with a valid instructor ID
    url = BASE + f"/api/admin/instructors/{instructor_id}"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {admin_token}'}
    data = {"email": "updatedinstructor@iitm.ac.in", "password": "newpassword123"}
    response = requests.put(url, data=json.dumps(data), headers=headers)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for instructor not found
    instructor_id = 9999  # Replace with an invalid instructor ID
    url = BASE + f"/api/admin/instructors/{instructor_id}"
    response = requests.put(url, data=json.dumps(data), headers=headers)
    expected_status_code = 404
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

# Test cases for /api/admin/instructors/{id} (DELETE)
def test_delete_instructor():
    instructor_id = 1  # Replace with a valid instructor ID
    url = BASE + f"/api/admin/instructors/{instructor_id}"
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = requests.delete(url, headers=headers)
    
    # Expected outcome
    expected_status_code = 204
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for instructor not found
    instructor_id = 9999  # Replace with an invalid instructor ID
    url = BASE + f"/api/admin/instructors/{instructor_id}"
    response = requests.delete(url, headers=headers)
    expected_status_code = 404
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

if __name__ == "__main__":
    pytest.main()
    
    
    