from dtaidistance import dtw
import pandas as pd
import numpy as np
import time
def fingerprint_generate(file_name):
    train_pd = pd.read_csv("/Users/ljw/PycharmProjects/VideoFlowClassify/FeatureCSV/youtube_train_onoff.csv")
    train_pd.fillna(0,inplace=True)
    tag = np.array(train_pd.iloc[0,2:]).astype("double")
    cls_distance = {}
    cls_distance[0] = [0]
    for id in range(1,train_pd.size-1):
        cls = int(train_pd.iloc[id,1])
        print(cls)
        if cls_distance.keys().__contains__(cls):
            seg= np.array(train_pd.iloc[id,2:]).astype("double")
            start = time.time()
            dis = dtw.distance_fast(tag,seg)
            print(time.time()-start)
            cls_distance[int(train_pd.iloc[id,1])].append(dis)
        else:
            cls_distance[int(train_pd.iloc[id,1])] = [0]
            tag = np.array(train_pd.iloc[id, 2:]).astype("double")


    print(cls_distance)
if __name__ == '__main__':
    fingerprint_generate("")
