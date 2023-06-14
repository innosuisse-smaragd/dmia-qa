from model import Model
import json
from flask import Flask, request, Response
from waitress import serve

app = Flask(__name__)


@app.route("/answer", methods=["POST"])
def predict():
    args = request.json
    result = model.predict(args["text"])
    r = Response(
        response=json.dumps({"result": result}, ensure_ascii=False),
        status=200,
        content_type="application/json",
    )
    return r


if __name__ == "__main__":
    model = Model()
    # for production use
    serve(app, host="0.0.0.0", port=5000)
    # for development use
    # app.run(host="0.0.0.0", debug=True)
