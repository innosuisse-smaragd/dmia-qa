from model import Model
import json
from flask import Flask, request, Response, abort
from waitress import serve


app = Flask(__name__)


@app.route("/answer", methods=["POST"])
def predict():
    args = request.json
    try:
        result = model.predict(args["text"])
        r = Response(
            response=json.dumps({"result": result}, ensure_ascii=False),
            status=200,
            content_type="application/json",
        )
    except ValueError:
        abort(400, "Import must be longer than three words")
    except NotImplementedError:
        abort(501, "No answer found for this question.")
    return r


@app.route("/improve", methods=["POST"])
def improve():
    args = request.json
    model.save_wrong_prediction(args)
    return "OK", 200


if __name__ == "__main__":
    model = Model()
    # for production use
    serve(app, host="0.0.0.0", port=5000)
    # for development use
    # app.run(host="0.0.0.0", debug=True)
