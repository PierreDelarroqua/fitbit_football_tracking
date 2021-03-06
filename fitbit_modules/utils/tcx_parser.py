from lxml import objectify
import pandas as pd


class TcxParser:
    def __init__(self, root, namespace):
        self.root = root
        self.namespace = namespace

    def latitude_values(self):
        return [float(x.text) for x in self.root.xpath('//ns:Position/ns:LatitudeDegrees',
                                                       namespaces={'ns': self.namespace})]

    def longitude_values(self):
        return [float(x.text) for x in self.root.xpath('//ns:Position/ns:LongitudeDegrees',
                                                       namespaces={'ns': self.namespace})]

    def heart_rate_values(self):
        return [int(x.text) for x in self.root.xpath('//ns:HeartRateBpm/ns:Value',
                                                     namespaces={'ns': self.namespace})]

    def time_values(self):
        return [x.text for x in self.root.xpath('//ns:Time',
                                                namespaces={'ns': self.namespace})]

    def create_df_coords(self):
        # Zip in a list and create a df
        list_coords = list(zip(self.time_values(), self.latitude_values(),
                               self.longitude_values()))  # self.heart_rate_values()
        df_coords = pd.DataFrame(list_coords, columns=['time', 'latitude', 'longitude'])  # 'heart_rate'
        # Slice time with the format 'hh:mm:ss'
        df_coords['time'] = df_coords.time.apply(lambda x: x[11:19])
        return df_coords


def tcx_to_df(tcx_file_path):
    namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
    tree = objectify.parse(tcx_file_path)
    root = tree.getroot()
    tcx_parser = TcxParser(root, namespace)
    df_coords = tcx_parser.create_df_coords()
    return df_coords
