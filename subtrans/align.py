def align_subtitles(subtitles):
    new_subtitles = []
    timestamp_end = "00:00:00,000"

    for line in subtitles:
        if "-->" in line:
            timestamp_start, timestamp_end = line.strip().split(" --> ")
            new_subtitles.append(timestamp_start + " --> " + timestamp_end)
        else:
            new_subtitles.append(line)

    # 更新时间戳
    for i in range(1, len(new_subtitles)):
        if "-->" in new_subtitles[i]:
            new_subtitles[i] = (
                new_subtitles[i].split(" --> ")[0] + " --> " + timestamp_end
            )

    return new_subtitles


# 读取原始字幕文件
with open("1.srt", "r") as file:
    subtitles = file.readlines()

# 对齐字幕时间戳
new_subtitles = align_subtitles(subtitles)

# 将对齐后的字幕写入新文件
with open("aligned_subtitles.srt", "w") as file:
    file.writelines(new_subtitles)
