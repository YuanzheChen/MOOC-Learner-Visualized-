# /usr/bin/env python
import flask
# Note the blue print must be placed right after import flask
querier_api = flask.Blueprint('querier_api', __name__)

from frames.objects import FramePool
from redis_io import io

frame_pool = None


@querier_api.route("/")
def querier():
    global frame_pool
    frame_pool = FramePool()

    html = flask.render_template(
        'frames/querier.html',
    )
    return html


@querier_api.route("/_query_frame_pool")
def query_frame_poll():
    return flask.jsonify(result=frame_pool.publish())


@querier_api.route("/_clear_all_frames")
def query_clear_all_frames():
    global frame_pool
    frame_pool.clear()
    return flask.jsonify(result=True)
