from fastmcp import FastMCP

from music.music_generator import MusicGenerator

import os
import datetime


mcp = FastMCP(
    "music-generator"
)

# 启动时加载一次模型
generator = MusicGenerator()

@mcp.tool()
def generate_music(
    prompt:str
)->str:
    """
    Generate music from text prompt.
    Args:
        prompt:
            Music description.
    Returns:
        wav file path
    """

    os.makedirs(
        "outputs",
        exist_ok=True
    )
    filename = (
        datetime.datetime.now()
        .strftime(
            "outputs/music_%Y%m%d_%H%M%S.wav"
        )
    )
    path = generator.generate(
        prompt,
        filename
    )
    return path

if __name__=="__main__":

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )