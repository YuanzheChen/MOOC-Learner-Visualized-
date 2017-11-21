# /usr/bin/env python
import flask
process_api = flask.Blueprint('process_api', __name__)

from frames.objects import FramePool

frame_pool = None


@process_api.route("/split_and_match")
def process():
    global frame_pool
    frame_pool = FramePool()
    html = flask.render_template(
        'processing/split_and_match.html',
    )
    return html


@process_api.route("/_get_isolated_frames")
def get_isolated_frames():
    return flask.jsonify(result=frame_pool.publish_isolated())


@process_api.route("/_request_match_frames")
def request_match_frames():
    select_isolated_frame_ids = str(flask.request.args.get('select_isolated_frame_ids', None)).split(',')
    select_isolated_frame_ids = [int(selected_id) for selected_id in select_isolated_frame_ids]
    return flask.jsonify(result=frame_pool.match(select_isolated_frame_ids))