# Flask Backend Project Management Application

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. Go to Project Folder:
```bash
cd BackEnd
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
Windows
```bash
venv\Scripts\activate
```
macOS/Linux
```bash  
source venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Set up environment variables in a .env file:
```bash
GEMINI_API_KEY=<your-gemimin-api-key>
```

6. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```
## Running the Application
```bash
python run.py
```

## API Documentation

Present in apis.yaml file

Auth Token to hit System Administrator APIs is: 'Sys-Admin-Secret'