from flask import Flask, request, jsonify
from project.main_agent import run_agent

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    text = data.get('text') or data.get('input') or ''
    if not text:
        return jsonify({'error':'no text provided'}), 400
    try:
        resp = run_agent(text)
        return jsonify({'response': resp})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
