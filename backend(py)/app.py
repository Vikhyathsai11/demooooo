import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# === Configure Gemini ===
load_dotenv()  # Load environment variables from a .env file
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))  # Fetch the API key from the .env file
model = genai.GenerativeModel('gemini-1.5-pro')

app = Flask(__name__)

def generate_quiz_question(topic, difficulty):
    prompt = f"""
    Generate 1 multiple-choice quiz question on the topic "{topic}" with {difficulty} difficulty.
    Format:
    Question: <Your question>
    Options:
    A. <option A>
    B. <option B>
    C. <option C>
    D. <option D>
    Answer: <correct option letter>
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def parse_question(raw_text):
    lines = raw_text.split('\n')
    question, options, answer = "", {}, ""

    for line in lines:
        if line.startswith("Question:"):
            question = line.replace("Question:", "").strip()
        elif line.strip().startswith("A."):
            options['A'] = line.split("A.")[1].strip()
        elif line.strip().startswith("B."):
            options['B'] = line.split("B.")[1].strip()
        elif line.strip().startswith("C."):
            options['C'] = line.split("C.")[1].strip()
        elif line.strip().startswith("D."):
            options['D'] = line.split("D.")[1].strip()
        elif line.strip().startswith("Answer:"):
            answer = line.split("Answer:")[1].strip()

    return {
        "question": question,
        "options": options,
        "correct_answer": answer
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-question', methods=['POST'])
def generate_question():
    data = request.get_json()
    topic = data.get('topic')
    difficulty = data.get('difficulty')

    try:
        raw = generate_quiz_question(topic, difficulty)
        parsed = parse_question(raw)
        parsed['difficulty'] = difficulty
        return jsonify(parsed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
