import pandas
import numpy
from redis_io import io


class FeatureFrame(pandas.DataFrame):
    KEYS = [
        'user_id',
        'video_id',
        'feature_week',
    ]

    def __init__(self, data=None, fields=None, frame=None):
        if frame is None:
            if not isinstance(fields, list):
                raise ValueError("fields mush be a list")
            if not all(isinstance(f, str) for f in fields):
                raise ValueError("all fields must be strings")
            if (not isinstance(data, tuple)
               or not all(isinstance(row, tuple) for row in data)):
                raise ValueError("data mush be a tuple of tuples")
            if not data:
                super(FeatureFrame, self).__init__([{}])
            if not all(len(row) == len(data[0]) for row in data):
                raise ValueError("data has rows of different sizes")
            if len(fields) > len(data[0]):
                raise ValueError("number of fields is larger the number of columns")
            dicts = []
            for row in data:
                dicts.append({fields[i]: row[i] for i in range(len(fields))})
            super(FeatureFrame, self).__init__(dicts)
        if frame is not None:
            super(FeatureFrame, self).__init__(frame)

    def to_msgpack(self, path_or_buf=None, encoding='utf-8', **kwargs):
        return self.to_pandas_frame().to_msgpack(path_or_buf, encoding, **kwargs)

    def to_pandas_frame(self):
        return pandas.DataFrame(data=self)

    def to_console(self):
        with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
            print(self)

    def publish_dicts(self):
        df = self.to_pandas_frame()
        df['_id'] = range(len(self))
        return df.to_dict('records')

    def publish_dict(self):
        dicts = self.publish_dicts()
        return {d['_id']: {k: d[k] for k in d if k != '_id'}
                for d in dicts}

    def get_key_fields(self):
        fields = self.columns.values.tolist()
        return [f for f in fields if f in self.KEYS]

    def get_feature_fields(self):
        fields = self.columns.values.tolist()
        return [f for f in fields if f not in self.KEYS and f != '_id']

    def get_length(self):
        return len(self.index.tolist())

    def to_source_data(self):
        data = {}
        for f in self.columns.values.tolist():
            data[f] = self[f].tolist()
        return data


class FramePool:
    name_prefix = 'MLV::frame_pool::'

    def __init__(self):
        self.pool = io.load(self.name_prefix) if io.load(self.name_prefix) else []

    def get_redis_key(self, _id):
        return self.name_prefix + str(hash(str(_id)))

    def save(self, frame):
        if not isinstance(frame, FeatureFrame):
            raise ValueError("FramePool only accept FeatureFrame")
        io.raw_save(self.get_redis_key(len(self.pool)), frame.to_msgpack(compress='zlib'))
        _id = len(self.pool)
        self.pool.append(self.get_redis_key(len(self.pool)))
        io.save(self.name_prefix, self.pool)
        return _id

    def load(self, _id):
        frame = pandas.read_msgpack(io.raw_load(self.get_redis_key(_id)))
        return FeatureFrame(frame=frame)

    def size(self):
        return len(self.pool)

    def match(self, ids):
        if not isinstance(ids, list) and all(isinstance(_id, int) for _id in ids):
            raise ValueError("Frame ids must be a list of integers")
        frames = [self.load(_id) for _id in ids]
        list_of_keys = [set(frame.get_key_fields()) for frame in frames]
        if not all(keys == list_of_keys[0] for keys in list_of_keys):
            raise ValueError("Frames to match must have identical set of keys")
        keys = list(list_of_keys[0])
        matched = frames[0]
        list_of_features = [set(frame.get_feature_fields()) for frame in frames]
        for i in range(1, len(frames)):
            matched = pandas.merge(matched, frames[i], on=keys, how='inner')
        matched = FeatureFrame(frame=matched)
        self.save(matched)
        return True

    def publish(self):
        dicts = []
        for _id in range(len(self.pool)):
            d = dict()
            d['_id'] = _id
            frame = self.load(_id)
            d['keys'] = frame.get_key_fields()
            d['features'] = frame.get_feature_fields()
            d['length'] = frame.get_length()
            dicts.append(d)
        return dicts

    def publish_isolated(self):
        dicts = []
        for _id in range(len(self.pool)):
            d = dict()
            d['_id'] = _id
            frame = self.load(_id)
            d['keys'] = frame.get_key_fields()
            d['features'] = frame.get_feature_fields()
            d['length'] = frame.get_length()
            if len(d['features']) == 1:
                dicts.append(d)
        return dicts

    def publish_one(self, _id):
        if _id is None:
            return [{'_id': 0, 'name': 'Disable'}]
        frame = self.load(_id)
        features = frame.get_feature_fields()
        keys = frame.get_key_fields()
        if 'feature_week' in keys:
            features = ['feature_week'] + features
        return [{'_id': 0, 'name': 'Disable'}] + \
               [{'_id': i+1, 'name': feature}
                for i, feature in enumerate(features)]

    def get_data(self, _id, data_setting):
        frame = self.load(_id)
        length = frame.get_length()
        features = frame.get_feature_fields()
        keys = frame.get_key_fields()
        if 'feature_week' in keys:
            features = ['feature_week'] + features
        data = dict()
        for element in data_setting:
            if element['value'] == 0:
                data[element['name']] = [None] * length
            else:
                data[element['name']] = frame[features[element['value'] - 1]].tolist()
        return FeatureFrame(frame=data)

    def clear(self):
        io.delete(self.name_prefix)
        self.__init__()
