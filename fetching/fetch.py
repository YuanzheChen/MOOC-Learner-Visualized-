# /usr/bin/env python
import flask
# Note the blue print must be placed right after import flask
fetch_api = flask.Blueprint('fetch_api', __name__)

from connector import Connector
from redis_io import io

connector = None
feature_table_frame = None
feature_frame = None
feature_id_frame = None


@fetch_api.route("/")
def fetch():
    global connector
    cfg_mysql = io.load('MLV::config::cfg_mysql')
    if not cfg_mysql:
        return "No MySQL config dict provided"
    connector = Connector(cfg_mysql)
    connector.open_conn()
    html = flask.render_template(
        'fetching/fetch.html',
    )
    return html


@fetch_api.route("/_get_feature_tables")
def get_feature_tables():
    global feature_table_frame
    feature_table_frame = connector.get_feature_tables()
    return flask.jsonify(result=feature_table_frame.publish_dicts())


@fetch_api.route("/_get_features")
def get_features():
    selected_feature_table_id = int(flask.request.args.get('selected_feature_table_id', None))
    selected_feature_table = feature_table_frame.publish_dict()[selected_feature_table_id]['feature_table']
    io.save('selected_feature_table', selected_feature_table)
    global feature_id_frame
    feature_id_frame = connector.get_feature_ids(selected_feature_table)
    return flask.jsonify(result=feature_id_frame.publish_dicts())


@fetch_api.route("/_set_selected_features")
def set_selected_features():
    selected_feature_id_ids = str(flask.request.args.get('selected_feature_id_ids', None)).split(',')
    selected_feature_id_ids = [int(selected_id) for selected_id in selected_feature_id_ids]
    selected_feature_ids = [feature_id_frame.publish_dict()[selected_id]['feature_id']
                            for selected_id in selected_feature_id_ids]
    selected_feature_names = [feature_id_frame.publish_dict()[selected_id]['feature_name']
                              for selected_id in selected_feature_id_ids]
    io.save('selected_feature_ids', selected_feature_ids)
    io.save('selected_feature_names', selected_feature_names)
    selected_feature_table = str(io.load('selected_feature_table'))
    return flask.jsonify(result=connector.save_features(selected_feature_table,
                                                        selected_feature_ids,
                                                        selected_feature_names))


