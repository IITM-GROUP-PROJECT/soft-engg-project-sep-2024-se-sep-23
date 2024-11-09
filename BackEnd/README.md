
# THINGS TO DO AFTER CLONING THE REPO

1.initialize data base (one time or first time after you clonned run following command)

   -> flask db init

2. database migration (everytime you want model changes to reflect in the DB run the following commands)

   -> flask db migrate -m " your migration message. "
   -> flask db upgrade

3. installing requirements

   -> pip install -r requirements.txt

4. finally run the app

   -> python run.py


# IMPORTANT RULES FOR DEVELOPER

1. Make sure you dont include venv, migrations, instance, logs folders and .env file when you commit due to security reasons

2. Add your routes in app/routes/api_routes.py (please dont write entire logic inside api_routes.py)

3. To write Business/app logic use services/logic.py

4. To write utilites functions like any functions that dont have our business logics should be written inside utils/helpers.py

5. When writing data to DB or sending responses kindly serialise/de-serialise the data using marshmellow if you don't know about marshmellow
   kindly learn about it from youtube :)

6. Kindly log every actions in INFO, an example logging is the following

    # from flask import current_app
    # current_app.logger.info("Hello World")

7. Kindly setup your own .env file as per your github_token and gemini api integration and following is the structure

    DATABASE_URL= YOUR DB URL       # Example(sqlite:///app.db)
    LOG_LEVEL=INFO  # options: DEBUG, INFO, WARNING, ERROR, CRITICAL (not mandatory)
    SECRET_KEY= YOUR SECRET KEY
    GITHUB_TOKEN = YOUR PERSONAL ACCESS TOKEN
    GEMINI_API_KEY = YOUR GEMINI KEY # (kindly refer youtube how to create one)
    APP_DATA_JSON_PATH = STATIC APP DATA FILE PATH (not mandatory)

8. Always add newly added packages in requirements.txt file under BackEnd folder.

9. Do not delete or add any branch without (kannan) permission.

10 !!! DO NOT CHECK IN MAIN BRANCH AND DO NOT MERGE or COMMIT IN MAIN WITHOUT (Kannan) Permission.

11. always add clear commit message when you commit something

12. do not commit multiple changes once, always commit when you done with one feature or issue fix so that it will be easy to revert

13. adding new files or changing directory structure requires (kannan) permission



