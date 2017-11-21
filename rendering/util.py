import numpy

from frames.objects import FeatureFrame

COLOR_NAMES = {
    'aliceblue': '#F0F8FF',
    'antiquewhite': '#FAEBD7',
    'aqua': '#00FFFF',
    'aquamarine': '#7FFFD4',
    'azure': '#F0FFFF',
    'beige': '#F5F5DC',
    'bisque': '#FFE4C4',
    'black': '#000000',
    'blanchedalmond': '#FFEBCD',
    'blue': '#0000FF',
    'blueviolet': '#8A2BE2',
    'brown': '#A52A2A',
    'burlywood': '#DEB887',
    'cadetblue': '#5F9EA0',
    'chartreuse': '#7FFF00',
    'chocolate': '#D2691E',
    'coral': '#FF7F50',
    'cornflowerblue': '#6495ED',
    'cornsilk': '#FFF8DC',
    'crimson': '#DC143C',
    'cyan': '#00FFFF',
    'darkblue': '#00008B',
    'darkcyan': '#008B8B',
    'darkgoldenrod': '#B8860B',
    'darkgray': '#A9A9A9',
    'darkgreen': '#006400',
    'darkkhaki': '#BDB76B',
    'darkmagenta': '#8B008B',
    'darkolivegreen': '#556B2F',
    'darkorange': '#FF8C00',
    'darkorchid': '#9932CC',
    'darkred': '#8B0000',
    'darksalmon': '#E9967A',
    'darkseagreen': '#8FBC8F',
    'darkslateblue': '#483D8B',
    'darkslategray': '#2F4F4F',
    'darkturquoise': '#00CED1',
    'darkviolet': '#9400D3',
    'deeppink': '#FF1493',
    'deepskyblue': '#00BFFF',
    'dimgray': '#696969',
    'dodgerblue': '#1E90FF',
    'firebrick': '#B22222',
    'floralwhite': '#FFFAF0',
    'forestgreen': '#228B22',
    'fuchsia': '#FF00FF',
    'gainsboro': '#DCDCDC',
    'ghostwhite': '#F8F8FF',
    'gold': '#FFD700',
    'goldenrod': '#DAA520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#ADFF2F',
    'honeydew': '#F0FFF0',
    'hotpink': '#FF69B4',
    'indianred': '#CD5C5C',
    'indigo': '#4B0082',
    'ivory': '#FFFFF0',
    'khaki': '#F0E68C',
    'lavender': '#E6E6FA',
    'lavenderblush': '#FFF0F5',
    'lawngreen': '#7CFC00',
    'lemonchiffon': '#FFFACD',
    'lightblue': '#ADD8E6',
    'lightcoral': '#F08080',
    'lightcyan': '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgreen': '#90EE90',
    'lightgray': '#D3D3D3',
    'lightpink': '#FFB6C1',
    'lightsalmon': '#FFA07A',
    'lightseagreen': '#20B2AA',
    'lightskyblue': '#87CEFA',
    'lightslategray': '#778899',
    'lightsteelblue': '#B0C4DE',
    'lightyellow': '#FFFFE0',
    'lime': '#00FF00',
    'limegreen': '#32CD32',
    'linen': '#FAF0E6',
    'magenta': '#FF00FF',
    'maroon': '#800000',
    'mediumaquamarine': '#66CDAA',
    'mediumblue': '#0000CD',
    'mediumorchid': '#BA55D3',
    'mediumpurple': '#9370DB',
    'mediumseagreen': '#3CB371',
    'mediumslateblue': '#7B68EE',
    'mediumspringgreen': '#00FA9A',
    'mediumturquoise': '#48D1CC',
    'mediumvioletred': '#C71585',
    'midnightblue': '#191970',
    'mintcream': '#F5FFFA',
    'mistyrose': '#FFE4E1',
    'moccasin': '#FFE4B5',
    'navajowhite': '#FFDEAD',
    'navy': '#000080',
    'oldlace': '#FDF5E6',
    'olive': '#808000',
    'olivedrab': '#6B8E23',
    'orange': '#FFA500',
    'orangered': '#FF4500',
    'orchid': '#DA70D6',
    'palegoldenrod': '#EEE8AA',
    'palegreen': '#98FB98',
    'paleturquoise': '#AFEEEE',
    'palevioletred': '#DB7093',
    'papayawhip': '#FFEFD5',
    'peachpuff': '#FFDAB9',
    'peru': '#CD853F',
    'pink': '#FFC0CB',
    'plum': '#DDA0DD',
    'powderblue': '#B0E0E6',
    'purple': '#800080',
    'red': '#FF0000',
    'rosybrown': '#BC8F8F',
    'royalblue': '#4169E1',
    'saddlebrown': '#8B4513',
    'salmon': '#FA8072',
    'sandybrown': '#FAA460',
    'seagreen': '#2E8B57',
    'seashell': '#FFF5EE',
    'sienna': '#A0522D',
    'silver': '#C0C0C0',
    'skyblue': '#87CEEB',
    'slateblue': '#6A5ACD',
    'slategray': '#708090',
    'snow': '#FFFAFA',
    'springgreen': '#00FF7F',
    'steelblue': '#4682B4',
    'tan': '#D2B48C',
    'teal': '#008080',
    'thistle': '#D8BFD8',
    'tomato': '#FF6347',
    'turquoise': '#40E0D0',
    'violet': '#EE82EE',
    'wheat': '#F5DEB3',
    'white': '#FFFFFF',
    'whitesmoke': '#F5F5F5',
    'yellow': '#FFFF00',
    'yellowgreen': '#9ACD32'
}


def preprocess_input(s):
    try:
        s = int(s)
        return s
    except ValueError:
        pass
    try:
        s = float(s)
        return s
    except ValueError:
        pass
    try:
        s = str(s)
        return s
    except ValueError:
        pass
    return s


def process_form_input(form_type, form_dicts, form_input):
    for element_dict in form_dicts:
        element_id = element_dict['type']+'_'+form_type+'_'+element_dict['name']
        if (element_id + '_value') in form_input:
            element_dict['value'] = preprocess_input(form_input[element_id + '_value'])
        if (element_id + '_text') in form_input:
            element_dict['text'] = preprocess_input(form_input[element_id + '_text'])
    return form_dicts


def initialize_form_dicts(form_dicts):
    try:
        for element_dict in form_dicts:
            element_dict['value'] = element_dict['default']
        return form_dicts
    except KeyError:
        raise ValueError("Invalid form dictionary")


def gen_empty_data_frame_from_data_setting(data_setting):
    data_source_template = dict()
    for element_dict in data_setting:
        data_source_template[element_dict['name']] = []
    return FeatureFrame(frame=data_source_template)


def form_dicts_to_dict(form_dicts):
    form_dict = dict()
    for element_dict in form_dicts:
        form_dict[element_dict['name']] = {k: element_dict[k]
                                           for k in element_dict
                                           if k != 'name'}
    return form_dict


def color_name_to_code(color_name):
    if color_name not in COLOR_NAMES:
        return None
    else:
        return COLOR_NAMES[color_name]


def digitize(l, n_bin=None, space=None):
    if (not isinstance(l, list)
        or not all(isinstance(i, int)
                   or isinstance(i, float)
                   or isinstance(i, long)
                   for i in l)):
        raise ValueError("Digitize: Invalid input list")
    if not space:
        if not isinstance(n_bin, int):
            raise ValueError("Digitize: Invalid number of bins")
        hist, bin_edges = numpy.histogram(l, n_bin-1)
        return numpy.digitize(l, bin_edges)
    elif not n_bin:
        if not isinstance(l, list) or not all(isinstance(i, int) for i in space):
            raise ValueError("Digitize: invalid range")
        try:
            map = {v: i for i, v in enumerate(space)}
            return [map[i] for i in l]
        except KeyError:
            raise ValueError("Digitize: find value not in the given value space")
    else:
        raise ValueError("Digitize: must indicate number of bins or range")