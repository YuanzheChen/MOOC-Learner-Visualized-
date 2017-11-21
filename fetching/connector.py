import MySQLdb
import MySQLdb.cursors as cursors

from frames.objects import FeatureFrame, FramePool


class Connector(object):
    rep = None
    cfg_mysql = None
    conn = None

    def __init__(self, replacement):
        self.rep = replacement
        self.cfg_mysql = replacement

    def open_conn(self):
        self.conn = MySQLdb.connect(host=self.cfg_mysql['host'],
                                    port=self.cfg_mysql['port'],
                                    user=self.cfg_mysql['user'],
                                    passwd=self.cfg_mysql['password'],
                                    db=self.cfg_mysql['database'],
                                    cursorclass=cursors.SSCursor)

    def close_conn(self):
        self.conn.close()

    def get_feature_tables(self):
        cursor = self.conn.cursor()
        sql = "SELECT DISTINCT(feature_table) FROM {0}.feature_info" \
              .format(self.cfg_mysql['database'])
        cursor.execute(sql)
        data = cursor.fetchall()
        feature_table_frame = FeatureFrame(data, ['feature_table'])
        cursor.close()
        self.conn.commit()
        return feature_table_frame

    def get_feature_ids(self, selected_feature_table):
        cursor = self.conn.cursor()

        sql = "SELECT DISTINCT(feature_id) AS id, " \
              "(SELECT feature_name FROM {0}.feature_info WHERE {0}.feature_info.feature_id = id) FROM {0}.{1}" \
              .format(self.cfg_mysql['database'], selected_feature_table)
        cursor.execute(sql)
        data = cursor.fetchall()
        feature_id_frame = FeatureFrame(data, ['feature_id', 'feature_name'])
        cursor.close()
        self.conn.commit()
        return feature_id_frame

    def save_features(self, selected_feature_table, selected_feature_ids, selected_feature_names):
        frame_pool = FramePool()
        keys = self.parse_keys_from_table_name(selected_feature_table)
        for i in range(len(selected_feature_ids)):
            cursor = self.conn.cursor()
            feature_description = '[{}] {}'.format(str(selected_feature_ids[i]).zfill(3), selected_feature_names[i])
            sql = "SELECT {0}, feature_value FROM {1}.{2} WHERE feature_id = {3}" \
                  .format(', '.join(keys), self.cfg_mysql['database'], selected_feature_table, selected_feature_ids[i])
            cursor.execute(sql)
            data = cursor.fetchall()
            feature_frame = FeatureFrame(data, keys + [feature_description])
            frame_pool.save(feature_frame)
            cursor.close()
        self.conn.commit()
        return True

    @staticmethod
    def parse_keys_from_table_name(feature_table_name):
        mapping = {
            'user': 'user_id',
            'video': 'video_id',
            'long': 'feature_week',
        }
        return [mapping[abbr] for abbr in feature_table_name[:-8].split('_') if abbr in mapping]
