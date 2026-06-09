import google.generativeai as genai
from flask import Flask, request, render_template, jsonify
import pymysql
import os
from difflib import SequenceMatcher

app = Flask(__name__)

# Database Connection
db = pymysql.connect(host='localhost', user='root', password='', db='mockinterview',port=3306)
cursor = db.cursor()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")




genai.configure(api_key=GOOGLE_API_KEY)

# Selecting the appropriate model for content generation
model = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        model = genai.GenerativeModel('gemini-1.5-flash')
        break

def generate_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if ":" in response_text:
            response_text = response_text.split(":", 1)[-1].strip()
        return response_text
    except Exception as e:
        print("An error occurred:", e)
        return None



def fetch_next_question(role, current_question_id=None):
    query = """
        SELECT question_id, question_text 
        FROM question
        WHERE role_id = (SELECT role_id FROM roles WHERE role_name = %s)
    """
    if current_question_id:
        query += " AND question_id > %s"
        params = (role, current_question_id)
    else:
        params = (role,)
    query += " ORDER BY question_id ASC LIMIT 1"
    cursor.execute(query, params)
    next_question = cursor.fetchone()
    return next_question  # Returns (question_id, question_text) or None

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()






if __name__ == '__main__':
    app.run(debug=True)
