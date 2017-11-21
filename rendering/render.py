# /usr/bin/env python
import flask
import matplotlib.pyplot as pyplot
import mpld3
import pandas
import pandas.tools.plotting
import bokeh
import bokeh.resources
import bokeh.embed
from bokeh.util.string import encode_utf8
import StringIO

from matplotlib.backends.backend_agg import FigureCanvasAgg

render_api = flask.Blueprint('render_api', __name__)

import drawers
from forms import check_plot_type, initialize_forms, load_forms, load_config, load_data_setting, load_interaction_config, \
    save_config, save_data_setting, save_interaction_config, load_selected_frame_id, save_selected_frame_id
from util import process_form_input, gen_empty_data_frame_from_data_setting
from frames.objects import FramePool
from redis_io import io

frame_pool = None


@render_api.route("/_get_frames")
def get_frames():
    return flask.jsonify(result=frame_pool.publish())


@render_api.route("/_get_data_list")
def get_data_list():
    selected_frame_id = flask.request.args.get('selected_frame_id', None)
    data_list = frame_pool.publish_one(selected_frame_id)
    return flask.jsonify(result=data_list)


'''
Interactive Template
'''


@render_api.route("/interactive/<interactive_plot_type>")
def interactive_page(interactive_plot_type):
    if not check_plot_type(interactive_plot_type):
        return "Unsupported plot type"
    global frame_pool
    frame_pool = FramePool()
    initialize_forms(interactive_plot_type)
    try:
        (data_setting, config, interaction_config) = load_forms(interactive_plot_type)
    except ValueError:
        return "Requested plot is located under /render/static/"
    html = flask.render_template(
        'rendering/interactive_page.html',
        plot_type=interactive_plot_type,
        data_setting=data_setting,
        config=config,
        interaction_config=interaction_config,
    )
    return html


@render_api.route("/interactive/<interactive_plot_type>/_plot")
def interactive_plot(interactive_plot_type):
    (data_setting, config, interaction_config) = load_forms(interactive_plot_type)
    selected_frame_id = load_selected_frame_id(interactive_plot_type)
    if selected_frame_id is None:
        frame = gen_empty_data_frame_from_data_setting(data_setting)
    else:
        frame = frame_pool.get_data(selected_frame_id, data_setting)
    js_resources = bokeh.resources.INLINE.render_js()
    css_resources = bokeh.resources.INLINE.render_css()
    layout = drawers.draw(interactive_plot_type, frame, data_setting, config, interaction_config)
    script, div = bokeh.embed.components(layout)
    html = flask.render_template(
        'rendering/interactive_plot.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)


@render_api.route("/interactive/<interactive_plot_type>/_set_selected_frame")
def interactive_set_selected_frame(interactive_plot_type):
    selected_frame_id = flask.request.args.get('selected_frame_id', None)
    if selected_frame_id is None or selected_frame_id == '':
        selected_frame_id = None
    else:
        selected_frame_id = int(selected_frame_id)
    save_selected_frame_id(interactive_plot_type, selected_frame_id)
    return flask.jsonify(result=True)


@render_api.route("/interactive/<interactive_plot_type>/_get_data_setting")
def interactive_get_data_setting(interactive_plot_type):
    data_setting = load_forms(interactive_plot_type)[0]
    return flask.jsonify(result=data_setting)


@render_api.route("/interactive/<interactive_plot_type>/_set_data_setting")
def interactive_set_data_setting(interactive_plot_type):
    data_setting = load_data_setting(interactive_plot_type)
    data_setting_input = flask.request.args
    data_setting = process_form_input('data_setting', data_setting, data_setting_input)
    save_data_setting(interactive_plot_type, data_setting)
    return flask.jsonify(result=True)


@render_api.route("/interactive/<interactive_plot_type>/_get_config")
def interactive_get_config(interactive_plot_type):
    config = load_config(interactive_plot_type)
    return flask.jsonify(result=config)


@render_api.route("/interactive/<interactive_plot_type>/_set_config")
def interactive_set_config(interactive_plot_type):
    config = load_config(interactive_plot_type)
    config_input = flask.request.args
    config = process_form_input('config', config, config_input)
    save_config(interactive_plot_type, config)
    return flask.jsonify(result=True)


@render_api.route("/interactive/<interactive_plot_type>/_get_interaction_config")
def interactive_get_interaction_config(interactive_plot_type):
    interaction_config = load_interaction_config(interactive_plot_type)
    return flask.jsonify(result=interaction_config)


@render_api.route("/interactive/<interactive_plot_type>/_set_interaction_config")
def interactive_set_interaction_config(interactive_plot_type):
    interaction_config = load_interaction_config(interactive_plot_type)
    interaction_config_input = flask.request.args
    interaction_config = process_form_input('interaction_config', interaction_config, interaction_config_input)
    save_interaction_config(interactive_plot_type, interaction_config)
    return flask.jsonify(result=True)


@render_api.route("/interactive/<interactive_plot_type>/_query_cache", methods=['GET', 'POST'])
def interactive_query_cache(interactive_plot_type):
    (data_setting, config, interaction_config) = load_forms(interactive_plot_type)
    return flask.jsonify(dict(selected_frame_id=io.load('selected_frame_id'),
                              data_setting=data_setting,
                              config=config,
                              interation_config=interaction_config))


'''
Static Template
'''


@render_api.route("/static/<static_plot_type>")
def static_page(static_plot_type):
    if not check_plot_type(static_plot_type):
        return "Unsupported plot type"
    global frame_pool
    frame_pool = FramePool()
    initialize_forms(static_plot_type)
    try:
        (data_setting, config) = load_forms(static_plot_type)
    except ValueError:
        return "Requested plot is located under /render/interactive/"
    html = flask.render_template(
        'rendering/static_page.html',
        plot_type=static_plot_type,
        data_setting=data_setting,
        config=config,
    )
    return html


@render_api.route("/static/<static_plot_type>/_plot")
def static_plot(static_plot_type):
    (data_setting, config) = load_forms(static_plot_type)
    selected_frame_id = load_selected_frame_id(static_plot_type)
    if selected_frame_id is None:
        frame = gen_empty_data_frame_from_data_setting(data_setting)
    else:
        frame = frame_pool.get_data(selected_frame_id, data_setting)

    fig = drawers.draw(static_plot_type, frame, data_setting, config)
    plot_div = mpld3.fig_to_html(fig)
    html = flask.render_template(
        'rendering/static_plot.html',
        plot_div=plot_div,
    )
    return encode_utf8(html)


@render_api.route("/static/<static_plot_type>/_set_selected_frame")
def static_set_selected_frame(static_plot_type):
    selected_frame_id = flask.request.args.get('selected_frame_id', None)
    if selected_frame_id is None or selected_frame_id == '':
        selected_frame_id = None
    else:
        selected_frame_id = int(selected_frame_id)
    save_selected_frame_id(static_plot_type, selected_frame_id)
    return flask.jsonify(result=True)


@render_api.route("/static/<static_plot_type>/_get_data_setting")
def static_get_data_setting(static_plot_type):
    data_setting = load_forms(static_plot_type)[0]
    return flask.jsonify(result=data_setting)


@render_api.route("/static/<static_plot_type>/_set_data_setting")
def static_set_data_setting(static_plot_type):
    data_setting = load_data_setting(static_plot_type)
    data_setting_input = flask.request.args
    print(data_setting_input)
    data_setting = process_form_input('data_setting', data_setting, data_setting_input)
    save_data_setting(static_plot_type, data_setting)
    return flask.jsonify(result=True)


@render_api.route("/static/<static_plot_type>/_get_config")
def static_get_config(static_plot_type):
    config = load_config(static_plot_type)
    return flask.jsonify(result=config)


@render_api.route("/static/<static_plot_type>/_set_config")
def static_set_config(static_plot_type):
    config = load_config(static_plot_type)
    config_input = flask.request.args
    config = process_form_input('config', config, config_input)
    save_config(static_plot_type, config)
    return flask.jsonify(result=True)


@render_api.route("/static/<static_plot_type>/_query_cache", methods=['GET', 'POST'])
def static_query_cache(static_plot_type):
    (data_setting, config) = load_forms(static_plot_type)
    return flask.jsonify(dict(selected_frame_id=io.load('selected_frame_id'),
                              data_setting=data_setting,
                              config=config))
