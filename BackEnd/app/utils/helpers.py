# you can use this method to create common methods like encoder/decoder
import fitz
import os
import google.generativeai as genai


def ai_eval(data):
    try:

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        report = data.get('report')
        guidelines = data.get('guidelines')

        prompt = f"Evaluate the following Data based on the Guidelines. Guidelines: {guidelines}. Data: {report}"
        response = model.generate_content(prompt)
        response.status= True
        return response
    except Exception as e:
        response = {'error':str(e),'status':False}
        return response


def pdf_to_text(filepath):
    text = ""
    with fitz.open(filepath) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text("text")
    return text