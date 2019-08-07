import requests
from flask import Flask, request, Response
import os
import json
import datetime
import logger
from time import sleep

app = Flask(__name__)

logger = logger.Logger("delayed-rest-proxy", os.environ.get(
    "LOGLEVEL", "INFO"))

DELAY_DURATION_IN_SECONDS = int(
    os.environ.get("DELAY_DURATION_IN_SECONDS", 60))

OPERATIONS = json.loads(os.environ.get("OPERATIONS"))
URL_PATTERN = os.environ.get("URL_PATTERN")

logger.info(
    "starting service with URL_PATTERN=%s, DELAY_DURATION_IN_SECONDS=%d, OPERATIONS=%s"
    % (URL_PATTERN, DELAY_DURATION_IN_SECONDS, OPERATIONS))
methods = [
    "GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "CONNECT", "PATCH",
    "TRACE"
]


def generate_response(response_text, status_code, content_type):
    return Response(
        response=response_text, status=status_code, content_type=content_type)


@app.route("/", methods=methods)
def proxy(path=""):
    try:
        is_first = True
        s = requests.Session()
        s.verify = False
        for entity in request.get_json():
            if not is_first:
                sleep(DELAY_DURATION_IN_SECONDS)
            is_first = False
            operation = OPERATIONS.get(entity.get("operation"))
            payload = entity.get("payload")
            logger.debug((URL_PATTERN % operation.get("url")) +
                         "Handling operation=%s, payload=%s" %
                         (operation, payload))
            r = s.request(
                method=operation.get("method"),
                url=(URL_PATTERN % operation.get("url")),
                headers=operation.get("headers"),
                params=request.args.items(),
                json=payload)

        return generate_response(
            json.dumps({
                "is_success": True,
                "message": ""
            }), 200, "application/json")

    except Exception as e:
        logger.exception(e)
        return generate_response(
            json.dumps({
                "is_success": False,
                "message": str(e)
            }), 500, "application/json")


if __name__ == '__main__':
    app.run(
        threaded=True,
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)))
