def split_string(s, n):
    # 步骤1: 计算每个分段的长度
    len_each_segment = len(s) // n

    # 步骤2: 找出每个分段的初步结束位置
    preliminary_end_positions = [len_each_segment * i for i in range(1, n)]

    # 步骤3: 找出每个分段的实际结束位置
    actual_end_positions = []
    for pos in preliminary_end_positions:
        forward_pos, backward_pos = pos, pos
        # 向前或向后搜索，直到找到','或'。'
        while forward_pos < len(s) and s[forward_pos] not in "。，":
            forward_pos += 1
        while backward_pos >= 0 and s[backward_pos] not in "。，":
            backward_pos -= 1
        # 选择更接近的位置
        if forward_pos - pos < pos - backward_pos:
            actual_end_positions.append(forward_pos)
        else:
            actual_end_positions.append(backward_pos)

    # 添加最后的位置
    actual_end_positions.append(len(s))

    # 步骤4: 分割字符串
    segments = []
    start = 0
    for end in actual_end_positions:
        # 在末尾包括逗号或句号
        segments.append(s[start : end + 1])
        # 从逗号或句号后的位置开始
        start = end + 1

    return segments


def parse_srt(filename):
    # 解析SRT文件，并将其切割成段落
    with open(filename, "r", encoding="utf-8") as file:
        srt_file = file.read()
        srt_file = srt_file.strip().split("\n\n")
    return srt_file


def write_translated_srt(translated_srt, filename):
    # 写入翻译后的SRT文件
    with open(filename, "w", encoding="utf-8") as file:
        for paragraph in translated_srt:
            for line in paragraph:
                file.write(line)
                file.write("\n")
            file.write("\n")
