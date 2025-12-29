from flask import Flask, request, jsonify
from flask_cors import CORS
from generation.answer_generator import AnswerGenerator
from monitoring.latency_tracker import track_latency

app = Flask(__name__)
CORS(app)

agent = AnswerGenerator()

@app.route('/')
def read_root():
    return {"message": "Welcome to Enterprise GenAI Platform API"}

@app.route('/health')
def health_check():
    return {"status": "healthy"}

@app.route('/query', methods=['POST'])
@track_latency
def query_llm():
    try:
        data = request.get_json()
        question = data.get('question')
        if not question:
            return jsonify({"error": "Question is required"}), 400
        answer = agent.answer(question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Error generating answer: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)