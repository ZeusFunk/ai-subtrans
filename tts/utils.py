from datetime import datetime
import os
from pydub.playback import play
from pydub import AudioSegment
import yaml
from subtrans.utils import parse_srt


def get_time(time_str1, time_str2):
    # 提取出开始和结束时间
    start_time_str1, end_time_str1 = time_str1.split(" --> ")
    start_time_str2, end_time_str2 = time_str2.split(" --> ")

    # 将字符串转化为datetime对象，注意毫秒是使用逗号分隔的，所以需要替换为点
    start_time1 = datetime.strptime(start_time_str1.replace(",", "."), "%H:%M:%S.%f")
    # end_time1 = datetime.strptime(end_time_str1.replace(',', '.'), "%H:%M:%S.%f")
    # start_time2 = datetime.strptime(start_time_str2.replace(',', '.'), "%H:%M:%S.%f")
    end_time2 = datetime.strptime(end_time_str2.replace(",", "."), "%H:%M:%S.%f")

    # 进行时间的减法运算
    time_diff = end_time2 - start_time1
    total_seconds = time_diff.total_seconds()
    return total_seconds


def get_number_from_filename(filenames):
    return int(filenames.replace(".wav", ""))


def merge_audio():
    # 再次读取配置文件
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # 1.获得字幕序列并解析计算时长
    srt_file = parse_srt(config["origin"])
    new_srt = []

    for line in srt_file:
        line = line.split("\n")
        new_srt.append(line)

    # 2.获取音频文件名称
    filenames = []
    for root, dirs, files in os.walk("./audio"):
        for file in files:
            filenames.append(file)
    sorted_file_names = sorted(filenames, key=get_number_from_filename)

    finalSound = AudioSegment.empty()
    # 3计算对应时长
    for i in range(0, len(srt_file), config["interval"]):
        timeReal = get_time(new_srt[i][1], new_srt[i + config["interval"] - 1][1])
        indexOfFile = int((i) / config["interval"])

        # 讀取文件
        sound = AudioSegment.from_file(f"./audio/{sorted_file_names[indexOfFile]}")

        silence_ms = timeReal - len(sound) * 1000  # ms
        silence = AudioSegment.silent(duration=silence_ms)

        finalSound += sound
        finalSound += silence

    finalSound.export("./audio/final.wav", format="wav")
