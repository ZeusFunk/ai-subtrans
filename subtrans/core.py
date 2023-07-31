import asyncio
import requests
import json
import yaml
import subtrans.utils
from concurrent.futures import ThreadPoolExecutor
from tts.tts import tts
from tts.utils import get_time

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {config['apiKey']}",
}


def translate_text(text):
    data = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [
            {
                "role": "system",
                "content": "Translate everything I send into Chinese",
            },
            {"role": "user", "content": text},
        ],
    }
    response = requests.post(config["apiUrl"], headers=headers, data=json.dumps(data))
    return response.json()["choices"][0]["message"]["content"]


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


# 现在 translate_and_append 返回结果而不是直接修改 translated_srt
def translate_and_append(text, translated_lines):
    translated_paragraph = translate_text(text)

    if config["isTTS"]:
        # 这里估计得tts啦
        # 1.计算时长 一个interval的时间间隔
        timeLenth = get_time(
            translated_lines[0][1], translated_lines[len(translated_lines) - 1][1]
        )

        # 2.计算字数和句子数
        # 计算字数
        num_chars = (
            len(translated_paragraph.replace(" ", ""))
            - translated_paragraph.count("。")
            - translated_paragraph.count("，")
        )

        # 计算句子数量
        num_sentences = translated_paragraph.count("。") + translated_paragraph.count(
            "，"
        )

        # 3.计算倍率
        rate = round(
            (
                (
                    num_chars * 0.00797927
                    + num_sentences * 0.00019948
                    + timeLenth * -0.05542216
                )
                + 0.485532973136976
            )
            * 100
        )

        # 开始转换
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            tts(translated_paragraph, rate, f"./audio/{translated_lines[0][0]}.wav")
        )
        loop.close()

    translated_paragraph = subtrans.utils.split_string(
        translated_paragraph, len(translated_lines)
    )
    for i in range(len(translated_lines)):
        translated_lines[i].append(translated_paragraph[i])
    return translated_lines


def translate_srt(srt_file, interval=5, thread_count=config["thread"]):
    translated_srt = []

    # 创建一个 ThreadPoolExecutor 实例
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = []

        for i in range(0, len(srt_file), interval):
            paragraphs = srt_file[i : i + interval]
            text = ""
            translated_lines = []
            for j in range(len(paragraphs)):
                lines = paragraphs[j].split("\n")
                time_line = lines[1]
                translated_lines.append([lines[0], time_line])
                text_lines = lines[2:]
                text += " " + text_lines[0]

            future = executor.submit(translate_and_append, text, translated_lines)
            futures.append(future)

        # 收集结果
        for future in futures:
            translated_srt.extend(future.result())

    return translated_srt
