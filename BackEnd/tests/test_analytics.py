import pytest
import requests

BASE = "http://127.0.0.1:5000"

# Test cases for /api/project_stats (GET)
def test_get_project_stats():
    url = BASE + "/api/project_stats"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Check if the response contains the expected keys
    expected_keys = ['project_stats']
    actual_response = response.json()
    assert all(key in actual_response for key in expected_keys), f"Expected keys {expected_keys}, got {actual_response.keys()}"

# Test cases for /api/student_stats (GET)
def test_get_student_stats():
    url = BASE + "/api/student_stats"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Check if the response contains the expected keys
    expected_keys = ['completed_students_per_project', 'students_not_started_milestones', 'incomplete_reports']
    actual_response = response.json()
    assert all(key in actual_response for key in expected_keys), f"Expected keys {expected_keys}, got {actual_response.keys()}"

if __name__ == "__main__":
    pytest.main()