import matplotlib.pyplot as pyplot
pyplot.style.use('ggplot')
from matplotlib.figure import Figure
import numpy
import pandas
import pandas.tools.plotting
import bokeh.palettes
from bokeh.layouts import column
from bokeh.models import CustomJS, Slider
from bokeh.models import HoverTool
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.models import Range1d, LinearAxis
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure
from scipy.stats import gaussian_kde

from rendering.util import digitize
from util import form_dicts_to_dict, color_name_to_code


def draw(plot_type, frame, data_setting, config, interaction_config=None):
    if plot_type == 'scatter':
        return draw_scatter(frame, data_setting, config, interaction_config)
    elif plot_type == 'histogram':
        return draw_histogram(frame, data_setting, config, interaction_config)
    elif plot_type == 'scatter_matrix':
        return draw_scatter_matrix(frame, data_setting, config)


def draw_scatter(frame, data_setting, config, interaction_config):
    data_setting = form_dicts_to_dict(data_setting)
    config = form_dicts_to_dict(config)
    interaction_config = form_dicts_to_dict(interaction_config)

    fig = figure(title="Scatter: %s" % config['title']['value'],
                 background_fill_color=color_name_to_code(config['background_color']['value']),
                 x_axis_label=data_setting['x']['text'][6:],
                 y_axis_label=data_setting['y']['text'][6:],
                 tools='box_zoom,pan,save,hover,resize,reset,tap,wheel_zoom',
                 toolbar_location="above")
    tooltips = []
    for key in data_setting:
        if data_setting[key]['value'] != 0:
            tooltips.append((data_setting[key]['text'], "@"+key))
    hover = fig.select(dict(type=HoverTool))
    hover.tooltips = tooltips
    hover.mode = 'mouse'

    if data_setting['x']['value'] == 0 and data_setting['y']['value'] == 0:
        return column(fig)

    frame['x'].replace(to_replace={None: 0}, inplace=True)
    frame['y'].replace(to_replace={None: 0}, inplace=True)
    if data_setting['size']['value'] != 0:
        n_size = config['n_size']['value']
        min_size = config['min_size']['value']
        max_size = config['max_size']['value']
        size_digital = digitize(frame['size'].tolist(), n_bin=n_size)
        size_map = numpy.arange(min_size, max_size, (max_size-min_size)/float(n_size))
        size = [size_map[s-1] for s in size_digital]
        frame['size'] = size
    else:
        frame['size'].replace(to_replace={None: config['default_size']['value']}, inplace=True)
    if data_setting['color']['value'] != 0:
        color_mapper = LinearColorMapper(palette=config['palette']['value'],
                                         low=frame['color'].min(),
                                         high=frame['color'].max())
        source = ColumnDataSource(frame.to_source_data())
        fig.circle(x='x', y='y', color={'field': 'color', 'transform': color_mapper},
                   size='size', source=source, fill_alpha=0.4, line_alpha=0.6)
        color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))
        fig.add_layout(color_bar, 'right')
    else:
        frame['color'].replace(to_replace={None: color_name_to_code(config['default_color']['value'])}, inplace=True)
        source = ColumnDataSource(frame.to_source_data())
        fig.circle(x='x', y='y', color='color', size='size', source=source,
                   fill_alpha=0.4, line_alpha=0.6)
    if data_setting['slider']['value'] != 0:
        slider = Slider(start=interaction_config['slider_start']['value'],
                        end=interaction_config['slider_end']['value'],
                        value=interaction_config['slider_default']['value'],
                        step=interaction_config['slider_step']['value'],
                        title=interaction_config['slider_name']['value'])
        original_source = ColumnDataSource(frame.to_source_data())
        javascript_body = """
                var v = cb_obj.value;
                var data = source.data;
                var original_data = original_source.data;
                var x = original_data.x;
                var y = original_data.y;
                var color = original_data.color;
                var size = original_data.size;
                var slider = original_data.slider;
                var new_x = [];
                var new_y = [];
                var new_color = [];
                var new_size = [];
                var new_slider = [];
                for ( i in slider ) {
                    if ( slider[i] %s v ) {
                        new_x.push(x[i]);
                        new_y.push(y[i]);
                        new_color.push(color[i]);
                        new_size.push(size[i]);
                        new_slider.push(slider[i]);
                    }
                }
                data.x = new_x;
                data.y = new_y;
                data.color = new_color;
                data.size = new_size;
                data.slider = new_slider;
                source.change.emit();
            """
        if interaction_config['slider_function']['value'] == 'filter':
            callback = CustomJS(args=dict(source=source, original_source=original_source), code=javascript_body % '>')
        else:
            callback = CustomJS(args=dict(source=source, original_source=original_source), code=javascript_body % '==')
        slider.js_on_change('value', callback)
        layout = column(slider, fig)
    else:
        layout = column(fig)
    return layout


def draw_histogram(frame, data_setting, config, interaction_config):
    data_setting = form_dicts_to_dict(data_setting)
    config = form_dicts_to_dict(config)
    interaction_config = form_dicts_to_dict(interaction_config)
    fig = figure(title="Histogram: %s" % config['title']['value'],
                 background_fill_color=color_name_to_code(config['background_color']['value']),
                 x_axis_label=(((data_setting['data1']['text'][6:]
                                if data_setting['data1']['value'] != 0
                                else '')
                               + ' & ' +
                               (data_setting['data2']['text'][6:]
                                if data_setting['data2']['value'] != 0
                                else ''))
                 if not (data_setting['data1']['value'] == 0
                         and
                         data_setting['data2']['value'] == 0)
                 else 'Disable').strip(' & '),
                 y_axis_label='Frequency',
                 tools='box_zoom,pan,save,hover,resize,reset,tap,wheel_zoom',
                 toolbar_location="above")
    tooltips = []
    for key in data_setting:
        if data_setting[key]['value'] != 0:
            tooltips.append((data_setting[key]['text'], "$"+key))
    hover = fig.select(dict(type=HoverTool))
    hover.tooltips = tooltips
    hover.mode = 'mouse'

    if data_setting['data1']['value'] == 0 and data_setting['data2']['value'] == 0:
        return column(fig)

    if data_setting['data1']['value'] != 0:
        hist1, edges1 = numpy.histogram(frame['data1'].tolist(), density=False,
                                        bins=config['n_bin']['value'])
        fig.quad(top=hist1, bottom=0, left=edges1[:-1], right=edges1[1:],
                 fill_color=color_name_to_code(config['fill_color1']['value']),
                 line_color=color_name_to_code(config['line_color1']['value']),
                 fill_alpha=0.4, line_alpha=0.6)
    if data_setting['data2']['value'] != 0:
        hist2, edges2 = numpy.histogram(frame['data2'].tolist(), density=False,
                                        bins=config['n_bin']['value'])
        fig.quad(top=hist2, bottom=0, left=edges2[:-1], right=edges2[1:],
                 fill_color=color_name_to_code(config['fill_color2']['value']),
                 line_color=color_name_to_code(config['line_color2']['value']),
                 fill_alpha=0.4, line_alpha=0.6)

    fig.y_range = Range1d(start=0,
                          end=max(
                              max(hist1)
                              if data_setting['data1']['value'] != 0
                              else 0,
                              max(hist2)
                              if data_setting['data2']['value'] != 0
                              else 0,
                          ))

    if (((config['show_pdf1']['value'] or config['show_cdf1']['value'])
         and data_setting['data1']['value'] != 0)
        or ((config['show_pdf2']['value'] or config['show_cdf2']['value'])
            and data_setting['data2']['value'] != 0)):
        fig.extra_y_ranges = {
            "normalized": Range1d(start=0, end=config['max_probability']['value'])
        }
        fig.add_layout(LinearAxis(y_range_name="normalized", axis_label='Probability'), 'right')
        samples = numpy.linspace(min(edges1[0] if data_setting['data1']['value'] != 0 else float('inf'),
                                     edges2[0] if data_setting['data2']['value'] != 0 else float('inf')),
                                 max(edges1[-1] if data_setting['data1']['value'] != 0 else float('-inf'),
                                     edges2[-1] if data_setting['data2']['value'] != 0 else float('-inf')),
                                 config['n_bin']['value'] * 10)
        if ((config['show_pdf1']['value'] or config['show_cdf1']['value'])
           and data_setting['data1']['value'] != 0):
            dist1 = gaussian_kde(frame['data1'].tolist())
            if config['show_pdf1']['value']:
                pdf1 = dist1.pdf(samples)
                fig.line(samples, pdf1, y_range_name="normalized",
                         line_color=color_name_to_code(config['pdf_color1']['value']),
                         line_width=config['line_width']['value'],
                         alpha=0.7, legend="PDF1")
            if config['show_cdf1']['value']:
                cdf1 = [dist1.integrate_box_1d(0, x) for x in samples]
                fig.line(samples, cdf1, y_range_name="normalized",
                         line_color=color_name_to_code(config['cdf_color1']['value']),
                         line_width=config['line_width']['value'],
                         alpha=0.7, legend="CDF1")
        if ((config['show_pdf2']['value'] or config['show_cdf2']['value'])
            and data_setting['data2']['value'] != 0):
            dist2 = gaussian_kde(frame['data2'].tolist())
            if config['show_pdf2']['value']:
                pdf2 = dist2.pdf(samples)
                fig.line(samples, pdf2, y_range_name="normalized",
                         line_color=color_name_to_code(config['pdf_color2']['value']),
                         line_width=config['line_width']['value'],
                         alpha=0.7, legend="PDF2")
            if config['show_cdf2']['value']:
                cdf2 = [dist2.integrate_box_1d(0, x) for x in samples]
                fig.line(samples, cdf2, y_range_name="normalized",
                         line_color=color_name_to_code(config['cdf_color2']['value']),
                         line_width=config['line_width']['value'],
                         alpha=0.7, legend="CDF2")

    # TODO: Add slider interaction to histogram by using two data source, one for ploting, on for indexing
    layout = column(fig)
    return layout


def draw_scatter_matrix(frame, data_setting, config):
    data_setting = form_dicts_to_dict(data_setting)
    config = form_dicts_to_dict(config)

    if all(data_setting[key]['value'] == 0 for key in data_setting):
        return Figure()

    for key in data_setting:
        if key == 'color':
            continue
        if data_setting[key]['value'] == 0:
            frame.drop(key, axis=1, inplace=True)
        else:
            frame.rename(columns={key: data_setting[key]['text']}, inplace=True)

    if data_setting['color']['value'] != 0:
        n_color = config['n_color']['value']
        color_digital = digitize(frame['color'].tolist(), n_bin=n_color)
        color_map = bokeh.palettes.inferno(n_color)
        color = [color_map[c-1] for c in color_digital]
    else:
        color = color_name_to_code(config['default_dot_color']['value'])
    pandas.tools.plotting.scatter_matrix(frame, color=color,
                                         alpha=0.6, figsize=(7, 7), diagonal='kde')
    return pyplot.gcf()
