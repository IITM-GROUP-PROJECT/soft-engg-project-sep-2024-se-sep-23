import pytest
import requests

BASE = "http://127.0.0.1:5000"

# Test cases for /api/prof/projects/{project_id} (GET)
def test_get_project():
    project_id = 1  
    url = BASE + f"/api/prof/projects/{project_id}"
    response = requests.get(url)
    
    # Expected outcome
    expected_status_code = 200
    
    # Actual output
    actual_status_code = response.status_code
    
    # Result
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

    # Test for project not found
    project_id = 9999  # Replace with an invalid project ID
    url = BASE + f"/api/prof/projects/{project_id}"
    response = requests.get(url)
    expected_status_code = 404
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f"Expected {expected_status_code}, got {actual_status_code}"

if __name__ == "__main__":
    pytest.main()
    