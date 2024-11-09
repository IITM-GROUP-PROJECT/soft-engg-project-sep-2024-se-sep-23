# IITM BS Degree Project Management App

This is a project management application developed for students enrolled in the IITM BS degree program. The application is structured with two main components: the `Frontend` and the `Backend`, each with its own folder.

---

## Getting Started

Please follow the setup instructions below to get both the frontend and backend services running on your local environment.


## Project Structure

The app's folder structure is organized as follows:

- `Frontend`: Contains the frontend code, built with Vue.js and served by a Flask API.
- `Backend`: Contains the backend API built with Flask.

---

## Setup Instructions

### Frontend

1. **Navigate to the frontend directory**:
    ```bash
    cd Frontend/vue-flask-app
    ```
2. **Install frontend dependencies**:
    ```bash
    npm install
    ```
3. **Run the frontend server**:
    ```bash
    npm run serve
    ```

### Backend

1. **Navigate to the backend directory**:
    ```bash
    cd BackEnd
    ```
2. **Install backend dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Set up the database**:
    - Initialize the database (only required the first time):
      ```bash
      flask db init
      ```
    - Run migrations:
      - To create a migration with a message:
         ```bash
         flask db migrate -m "your migration message"
         ```
      - Apply the migration to upgrade the database:
         ```bash
         flask db upgrade
         ```
4. **Run the backend server**:
    ```bash
    python run.py
    ```
