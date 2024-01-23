from flask import Flask, request, jsonify
from transformers import pipeline

# model
model_qa = pipeline(
    'question-answering',
    model='distilbert_bertqa',
    device=0
)

# API - use POSTMAN to test
app = Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        return jsonify({"response": "Give me an context and a question!"})
    elif request.method == "POST":
        req_json = request.json
        context = req_json['context']
        question = req_json['question']
        answer = model_qa(context=context, question=question)
        return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, port=9090)