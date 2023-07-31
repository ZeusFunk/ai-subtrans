import edge_tts


async def tts(TEXT, rate, output):
    fRate = ""
    if rate >= 0:
        fRate = f"+{rate}%"
    else:
        fRate = f"{rate}%"
    communicate = edge_tts.Communicate(TEXT, "zh-CN-XiaoxiaoNeural", rate=fRate)
    await communicate.save(output)
