# here we will create all business logic like how we process all app data
from app.utils import helpers
import json
import os
from dotenv import load_dotenv


load_dotenv()


def process_project_report(filepath):
    report = helpers.pdf_to_text(filepath)
    guidelines = load_static_data().report_eval_prompt
    data = {"report":report,"guidelines": guidelines}
    response = helpers.ai_eval(data)

    if not response.status:
        return "Error while processing report with Gemini, Contact Support "
    else:
        return  response.text



def load_static_data():
    with open(os.getenv("APP_DATA_JSON_PATH", "app/resources/application_data.json")) as file:
        data = json.load(file)
    return data