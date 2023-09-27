# -*- coding: utf-8 -*-

import os
import pickle
import pandas as pd
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, ".."))
from DataProcess.extract_burst import get_serial

bilibili_train_path = "/home/ljw/ml/VideoClassify/FeatureCSV/bilibili_train.csv"
youtube_train_path = "/home/ljw/ml/VideoClassify/FeatureCSV/youtube_train.csv"
youtube_delay_100_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/delay_100ms.csv"
youtube_delay_300_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/delay_300ms.csv"
youtube_delay_600_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/delay_600ms.csv"
youtube_delay_900_ms = "/home/ljw/ml/VideoClassify/FeatureCSV/delay_900ms.csv"
youtube_drop_1percent = "/home/ljw/ml/VideoClassify/FeatureCSV/drop_1Percent.csv"
youtube_drop_3percent = "/home/ljw/ml/VideoClassify/FeatureCSV/drop_3Percent.csv"
youtube_drop_6percent = "/home/ljw/ml/VideoClassify/FeatureCSV/drop_6Percent.csv"
youtube_drop_9percent = "/home/ljw/ml/VideoClassify/FeatureCSV/drop_9Percent.csv"


def csv_to_burst(dir_path,csv_path):
    title_dic = {}
    title_max = {}
    print("extract max stream")
    for root, dirs, files in os.walk(dir_path):
        for file in files:
           file_path_name = os.path.join(root, file)
           file_tuple = file_path_name.split("/")
           title_id_tf = file_tuple[-1]
           if title_id_tf.__contains__(".DS_Store"):
               continue
           title_id = file_tuple[-2]
           title = file_tuple[-3]
           if not title_dic.keys().__contains__(title):
               title_dic[title] = {}
               title_dic[title][title_id] = [file_path_name]
           elif  not title_dic[title].keys().__contains__(title_id):
                   title_dic[title][title_id] = [file_path_name]
           else:
               title_dic[title][title_id].append(file_path_name)
    for title_key in title_dic.keys():
        for title_id_key in title_dic[title_key].keys():
            max = 0
            max_file_name = ""
            for name in title_dic[title_key][title_id_key]:
                if os.path.getsize(name) > max:
                    max = os.path.getsize(name)
                    max_file_name = name
            if not title_max.keys().__contains__(title_key):
                title_max[title_key] = [max_file_name]
            else:
                title_max[title_key].append(max_file_name)
            print(max_file_name)
    data_serials = []
    cls_to_num = {}
    cls = 0
    print("extract stream to burst")
    for key in title_max.keys():
        cls_to_num[cls] = key
        for name in title_max[key]:
            try:
                serial = get_serial("",name)
                serial.insert(0, cls)
                data_serials.append(serial)
            except:
                continue
        cls = cls+1
    train_dataframe = pd.DataFrame(data_serials)
    train_dataframe.fillna(0, inplace=True)
    train_dataframe.rename(columns={0: "labels"}, inplace=True)
    train_dataframe.reset_index()
    train_dataframe['id'] = range(len(train_dataframe))
    train_dataframe.to_csv(csv_path)

    cls_file = open("/home/ljw/ml/VideoClassify/FeatureCSV/youtube_class","wb")
    pickle.dump(cls_to_num,cls_file)

    print(train_dataframe)

csv_to_burst("/mnt/video_pcap/title_fp_result/dataset_chrome_100",youtube_train_path)
