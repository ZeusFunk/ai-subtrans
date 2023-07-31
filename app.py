from subtrans.core import translate_srt
from subtrans.utils import parse_srt, write_translated_srt
import yaml
from tts.utils import merge_audio

# 读取配置文件
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

srt_file = parse_srt(config["origin"])
translated_srt = translate_srt(srt_file, interval=config["interval"])

if config["isTTS"]:
    merge_audio()

write_translated_srt(translated_srt, config["result"])
