# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import sys
import os
import pickle
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将需要导入模块代码文件相对于当前文件目录的绝对路径加入到sys.path中
sys.path.append(os.path.join(current_dir, ".."))
from DataProcess.extract_burst import get_serial
#from sklearn import preprocessing
from tsfresh import extract_relevant_features

video_class = {}
video_path = "/Users/ljw/Downloads/Videos_bitstream/CNNParsed"
train_path = "../FeatureCSV/train.csv"
youtube_train_top200_path = "../FeatureCSV/youtube_train_top200.csv"
youtube_train_path = "../FeatureCSV/youtube_train.csv"
bilibili_train = "../FeatureCSV/bilibili_train.csv"

youtube_delay_100_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/delay_100ms.csv"
youtube_delay_300_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/delay_300ms.csv"
youtube_delay_600_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/delay_600ms.csv"
youtube_delay_900_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/delay_900ms.csv"
youtube_drop_1percent = "/home/ljw/ml/VideoClassify/FeatureCSV/drop_1Percent.csv"
youtube_drop_3percent = "/home/ljw/ml/VideoClassify/FeatureCSV/drop_3Percent.csv"
youtube_drop_6percent = "/home/ljw/ml/VideoClassify/FeatureCSV/drop_6Percent.csv"
youtube_drop_9percent = "/home/ljw/ml/VideoClassify/FeatureCSV/drop_9Percent.csv"

bilibili_ts_feature_path = "../FeatureCSV/bilibili_ts_feature.csv"
ts_feature_path = "../FeatureCSV/ts_feature.csv"
youtube_ts_feature_path = "../FeatureCSV/youtube_ts_feature.csv"
youtube_ts_feature_top200_path = "../FeatureCSV/youtube_ts_feature_top200.csv"

youtube_ts_delay_100_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/ts_feature_delay_100ms.csv"
youtube_ts_delay_300_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/ts_feature_delay_300ms.csv"
youtube_ts_delay_600_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/ts_feature_delay_600ms.csv"
youtube_ts_delay_900_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/ts_feature_delay_900ms.csv"
youtube_ts_drop_1percent = "/home/ljw/ml/VideoClassify/FeatureCSV/ts_feature_drop_1Percent.csv"
youtube_ts_drop_3percent = "/home/ljw/ml/VideoClassify/FeatureCSV/ts_feature_drop_3Percent.csv"
youtube_ts_drop_6percent = "/home/ljw/ml/VideoClassify/FeatureCSV/ts_feature_drop_6Percent.csv"
youtube_ts_drop_9percent = "/home/ljw/ml/VideoClassify/FeatureCSV/ts_feature_drop_9Percent.csv"

def generate_train():
    class_num = 0
    train = np.zeros((4345,4501))
    index = 0
    for root, dirs, files in os.walk(video_path):
        for file in files:
            video = file.split(" ")[0]
            if '.' in video:
                video = file.split('.')[0]
            if not video_class.keys().__contains__(video):
                video_class[video] = class_num
                class_num = class_num+1
            video_burst = pd.read_csv(root+"/"+file)
            bytes = pd.array(video_burst["Bytes"])
            #print(bytes.shape)
            train[index][:4500] = bytes[:4500]
            train[index][4500] = video_class[video]
            print(train[index])
            index = index+1
    train_df = pd.DataFrame(train)
    train_df.reset_index()
    train_df['id'] = range(len(train_df))
    train_df.to_csv(train_path)
    print(train_df)

def ts_feature(train_dir,ts_dir):
    train_data = pd.read_csv(train_dir)

    label = train_data['labels'].astype(int)
    id = train_data['id']

    train_data = train_data.drop('labels',axis=1)
    train_data = train_data.drop('id', axis=1)

    data = train_data.astype(float).stack()
    data = data.reset_index()
    data = data.set_index("level_0")
    data.index.name = None
    data.rename(columns={"level_1": "time", 0: "bytes"}, inplace=True)
    data = data.join(id)

    #extract relevant feature
    extracted_features = extract_relevant_features(data, label,column_id='id', column_sort='time')
    feature_train = pd.concat([extracted_features, label], axis=1)
    #feature_train = feature_train.rename(columns={'4500':'label'},inplace=True)
    print(feature_train)
    #save feature to csv
    feature_train_pd = pd.DataFrame(feature_train)
    feature_train_pd.to_csv(ts_dir)

    # feature_size = feature_train_pd.columns.values.size
    # col = list(range(feature_size))
    # feature_id_dic = {}
    # for num in col:
    #     feature_id_dic[num] = feature_train_pd.columns.values[num]

    # feature_id_dic_file = open("/home/ljw/ml/VideoClassify/FeatureCSV/bilibili_feature_id.csv","wb")
    # pickle.dump(feature_id_dic,feature_id_dic_file)


if __name__ == '__main__':
    #trans_csv_burst("/Users/ljw/PycharmProjects/VideoFlowClassify/title_fp_result_traffic/VideoResult")
    ts_feature(youtube_delay_100_ms,youtube_ts_delay_100_ms)
    ts_feature(youtube_delay_300_ms,youtube_ts_delay_300_ms)
    ts_feature(youtube_delay_600_ms,youtube_ts_delay_600_ms)
    ts_feature(youtube_delay_900_ms,youtube_ts_delay_900_ms)
    ts_feature(youtube_drop_1percent,youtube_ts_drop_1percent)
    ts_feature(youtube_drop_3percent,youtube_ts_drop_3percent)
    ts_feature(youtube_drop_6percent,youtube_ts_drop_6percent)
    ts_feature(youtube_drop_9percent,youtube_ts_drop_9percent)