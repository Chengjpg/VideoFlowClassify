import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.parasite_axes import HostAxes,ParasiteAxes
import os

interval = 0.25;
def get_serial(path, file_name):
    video_result = "/".join((path, file_name))
    video_result_csv = pd.read_csv(video_result)
    video_result_csv.sort_values(by="timestamp", inplace=True)
    num = 1
    start = 0
    len = 0
    size = 0
    serial = []

    for index,row in video_result_csv.iterrows():
        timeStamp,pcapLen = row["timestamp"],row["pkt_len"]
        if start==0:
            start = timeStamp
        #print("{},{}".format(timeStamp,start))
        if float(timeStamp)-float(start) < interval:
            len += pcapLen
            size += 1
        else:
            #serial.append([num * interval, len, size, float(len) / size])
            serial.append(len)
            start += interval
            len = pcapLen
            size = 1
            num+=1
    return serial

def get_serial_onoff(path,file_name):
    video_result = "/".join((path, file_name))
    video_result_csv = pd.read_csv(video_result)
    video_result_csv.sort_values(by="timestamp", inplace=True)
    len = 0
    no = 0
    serial = []
    for index, row in video_result_csv.iterrows():
        pcapLen,dir = row["pkt_len"],row["dir"]
        if dir == 0:
            len += pcapLen
        else:
            serial.append([no, len])
            len = 0
            no += 1
    return serial

def draw_onoff(serial,fileName):
    data = np.array(serial)
    data = data.T
    fig = plt.figure(figsize=(24, 16))
    title = "{}'s_video_feature_onoff".format(fileName)
    plt.title(title)
    plt.bar(data[0], data[1], width=0.05,label="size")
    fig.savefig("../Figures/Onoff/{}.png".format(title))

def draw_burst(serial, fileName):
    data = np.array(serial)
    data = data.T
    fig = plt.figure(figsize=(24,16))
    ax_size = HostAxes(fig,[0.05,0.05,0.8,0.8])

    ax_num = ParasiteAxes(ax_size,sharex=ax_size)
    ax_average = ParasiteAxes(ax_size,sharex=ax_size)

    ax_size.parasites.append(ax_num)
    ax_size.parasites.append(ax_average)
    ax_size.axis['right'].set_visible(False)
    ax_size.axis['top'].set_visible(False)

    ax_num.axis['right'].set_visible(True)
    ax_num.axis['right'].major_ticklabels.set_visible(True)
    ax_num.axis['right'].label.set_visible(True)

    ax_size.set_ylabel('size')
    ax_size.set_xlabel('Interval')
    ax_num.set_ylabel('num')
    ax_average.set_ylabel('average')

    average_axisline = ax_average.get_grid_helper().new_fixed_axis
    ax_average.axis['right2'] = average_axisline(loc='right', axes=ax_average, offset=(60,0))
    fig.add_axes(ax_size)

    size,=ax_size.plot(data[0],data[1],label="size",color='black')
    num,=ax_num.plot(data[0],data[2],label="num",color='red')
    average,=ax_average.plot(data[0],data[3],label="average",color='green')

    ax_num.set_ylim(0,2000)
    ax_average.set_ylim(0,2000)
    ax_size.legend()

    ax_num.axis['right'].label.set_color('red')
    ax_average.axis['right2'].label.set_color('green')
    ax_num.axis['right'].major_ticks.set_color('red')
    ax_average.axis['right2'].major_ticks.set_color('green')

    ax_num.axis['right'].major_ticklabels.set_color('red')
    ax_average.axis['right2'].major_ticklabels.set_color('green')
    ax_num.axis['right'].line.set_color('red')
    ax_average.axis['right2'].line.set_color('green')
    title ="{}'s_video_feature_Interval_{}s".format(fileName, interval)
    plt.title(title)
    # plt.show()
    fig.savefig("../Figures/Burst/{}.png".format(title))
    data = np.array(serial)
    print(data)

def draw_complete():
    action1 = np.array(pd.read_csv("../FeatureCSV/Burst/up_action1.pcap.csv")).T
    action2 = np.array(pd.read_csv("../FeatureCSV/Burst/up_action2.pcap.csv")).T
    action3 = np.array(pd.read_csv("../FeatureCSV/Burst/up_action3.pcap.csv")).T
    action4 = np.array(pd.read_csv("../FeatureCSV/Burst/up_action4.pcap.csv")).T
    action5 = np.array(pd.read_csv("../FeatureCSV/Burst/up_action5.pcap.csv")).T
    static1 = np.array(pd.read_csv("../FeatureCSV/Burst/up_static1.pcap.csv")).T
    static2 = np.array(pd.read_csv("../FeatureCSV/Burst/up_static2.pcap.csv")).T
    static3 = np.array(pd.read_csv("../FeatureCSV/Burst/up_static3.pcap.csv")).T
    static4 = np.array(pd.read_csv("../FeatureCSV/Burst/up_static4.pcap.csv")).T
    static5 = np.array(pd.read_csv("../FeatureCSV/Burst/up_static5.pcap.csv")).T
    plt.figure(figsize=(24, 16))
    plt.plot(action1[1], action1[2], color='k',label="action1")
  #  plt.plot(action2[1], action2[2], color='r')
    plt.plot(action3[1], action3[2], color='k',label="action3")
    plt.plot(action4[1], action4[2], color='k',label="action4")
    plt.plot(action5[1], action5[2], color='k',label="action5")
    plt.plot(static1[1], static1[2], color='m',label="static1")
    plt.plot(static2[1], static2[2], color='m',label="static2")
    plt.plot(static3[1], static3[2], color='m',label="static3")
    plt.plot(static4[1], static4[2], color='m',label="static4")
    plt.plot(static5[1], static5[2], color='m',label="static5")
    plt.xlabel('time')
    plt.ylabel('size')
    plt.legend()
    plt.show()

def draw_floder(dir):
     walk = os.walk(dir)
     for path, dirList, files in walk:
         for fileName in files:
             print(path+fileName)
             serial = get_serial(path, fileName)
             data = np.array(serial)
             pd.DataFrame(data).to_csv('../FeatureCSV/Burst/{}'.format(fileName))
             draw_burst(serial,fileName)

if __name__ == '__main__':
    path = "../title_fp_result_traffic/VideoResult/_Katy_Perry_Birthday/"
    # fileName = "down_10_scenery.csv"
    # serial = GetSerial(path,fileName)
    # DrawBurst(serial,fileName)
    draw_floder(path)
   # draw_complete()

