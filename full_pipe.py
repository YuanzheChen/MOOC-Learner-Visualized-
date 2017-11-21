"""

"""
# /usr/bin/env python
from __future__ import print_function

import sys
import flask
import redis
import json

from fetching.fetch import fetch_api
from processing.process import process_api
from rendering.render import render_api
from frames.querier import querier_api
from config import config
from redis_io import io
from frames.objects import FramePool, FeatureFrame

app = flask.Flask(__name__)
# Entering Flask debug mode
# app.config['DEBUG'] = True

app.register_blueprint(fetch_api, url_prefix='/fetch')
app.register_blueprint(process_api, url_prefix='/process')
app.register_blueprint(render_api, url_prefix='/render')
app.register_blueprint(querier_api, url_prefix='/querier')

# open redis connection
rds = redis.StrictRedis(host='redis', port=6379, db=0)


@app.route('/')
def index():
    html = flask.render_template(
        'index.html',
    )
    return html


if __name__ == "__main__":
    rds.flushall()
    io.connect(rds)

    if len(sys.argv) < 2:
        cfg = config.ConfigParser()
    else:
        cfg = config.ConfigParser(sys.argv[1])
    if not cfg.is_valid():
        sys.exit("Config file is invalid.")
    cfg_mysql = cfg.get_or_query_mysql()
    io.save('MLV::config::cfg_mysql', cfg_mysql)

    frame_pool = FramePool()

    app.run(host='0.0.0.0')
