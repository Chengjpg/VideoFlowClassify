import pandas as pd

def get_serial_onoff(file_name):
    video_result_csv = pd.read_csv(file_name)
    serials = []
    for index, row in video_result_csv.iterrows():
        agg = []
        agg.append(row.iloc[1])
        size = 0
        for i in range(2,row.size):
            num = int(row.iloc[i])
            if num is not 0:
                size = size+num
            else:
                if size is not 0:
                    agg.append(size)
                size = 0
        print(agg)
        serials.append(agg)
    df = pd.DataFrame(serials)
    df.to_csv("/Users/ljw/PycharmProjects/VideoFlowClassify/FeatureCSV/youtube_train_onoff.csv")

if __name__ == '__main__':
    get_serial_onoff("/Users/ljw/PycharmProjects/VideoFlowClassify/FeatureCSV/youtube_train.csv")