import requests
from flask import Flask, request, Response
import os
import json
import datetime
import re
from time import sleep
from sesamutils import VariablesConfig, sesam_logger
from sesamutils.flask import serve
import sys
from werkzeug.routing import Rule

app = Flask(__name__)
app.url_map.add(Rule('/', endpoint='proxy'))

required_env_vars = ["OPERATIONS", "URL_PATTERN"]
optional_env_vars = [("DELAY_DURATION_IN_SECONDS", 60), "LOG_LEVEL"]
env_config = VariablesConfig(
    required_env_vars, optional_env_vars=optional_env_vars)

if not env_config.validate():
    sys.exit(1)

env_config.OPERATIONS = json.loads(env_config.OPERATIONS)
env_config.DELAY_DURATION_IN_SECONDS = int(env_config.DELAY_DURATION_IN_SECONDS)

logger = sesam_logger("delayed-rest-proxy", app=app)
logger.info(
    "starting service with \n\tURL_PATTERN=%s\n\tOPERATIONS=%s, \n\tDELAY_DURATION_IN_SECONDS=%d, \n\tLOG_LEVEL=%s"
    % (env_config.URL_PATTERN, env_config.OPERATIONS, env_config.DELAY_DURATION_IN_SECONDS, logger.level))


def generate_response(status_code, message):
    return Response(response=json.dumps({
        "is_success": (status_code >= 200 and status_code < 300),
        "message": message
    }), status=status_code, content_type="application/json")


def transit_decode(payload):
    if isinstance(payload, dict):
        transit_decoded_payload = {}
        for key, value in payload.items():
            transit_decoded_payload[key] = transit_decode(value)
    elif isinstance(payload, list):
        transit_decoded_payload = []
        for item in payload:
            transit_decoded_payload.append(transit_decode(item))
    else:
        transit_decoded_payload = None
        if payload and isinstance(payload, str):
            transit_decoded_payload = re.sub(r'~[:rtbuf]', '', payload)
        else:
            transit_decoded_payload = payload
    return transit_decoded_payload

@app.endpoint('proxy')
def proxy(path=""):
    try:
        is_first = True
        s = requests.Session()
        s.verify = False
        input_json = request.get_json()
        if isinstance(input_json, dict):
            input_json = [input_json]
        for entity in input_json:
            transfer_decoded_entity=transit_decode(entity)
            if not is_first:
                sleep(env_config.DELAY_DURATION_IN_SECONDS)
            is_first = False
            operation = env_config.OPERATIONS.get(entity.get("operation"))
            payload = transit_decode(entity.get("payload"))
            logger.debug("sending {} request for _id={} to url={}".format(operation.get("method"), transfer_decoded_entity.get("_id", "-"), (env_config.URL_PATTERN % operation.get("url"))))

            r = s.request(
                method=operation.get("method"),
                url=(env_config.URL_PATTERN % operation.get("url")),
                headers=operation.get("headers"),
                params=request.args.items(),
                json=payload)

        return generate_response(200, "")

    except Exception as e:
        logger.exception(e)
        return generate_response(500, str(e))


if __name__ == '__main__':
    serve(app)
