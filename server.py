from fastmcp import FastMCP
from music.music_generator import MusicGenerator
<<<<<<< Updated upstream
import os
import datetime

mcp = FastMCP(
    name="music-generator"
)

# 启动时加载一次模型
generator = MusicGenerator()

@mcp.tool()
def generate_music(prompt:str)->str:
    """
    Generate music from text prompt.
    Args:
        prompt:
            Music description.
    Returns:
        wav file path
    """
=======

from contextlib import asynccontextmanager

import asyncio
import os
import uuid


# =====================
# Model
# =====================

generator = MusicGenerator()



# =====================
# Async Queue
# =====================

music_queue = asyncio.Queue()



async def music_worker():

    print("🎵 Music worker started")


    while True:

        prompt, filename, future = await music_queue.get()


        try:

            print(
                f"🎵 generating: {prompt}"
            )


            result = await asyncio.to_thread(
                generator.generate,
                prompt,
                filename
            )


            # 请求还存在
            if not future.cancelled():

                future.set_result(
                    result
                )


        except Exception as e:

            if not future.cancelled():

                future.set_exception(
                    e
                )


        finally:

            music_queue.task_done()



# =====================
# Lifespan
# =====================


@asynccontextmanager
async def lifespan(app):

    asyncio.create_task(
        music_worker()
    )

    yield



# =====================
# MCP
# =====================


mcp = FastMCP(
    name="music-generator",
    lifespan=lifespan
)



@mcp.tool()
async def generate_music(
    prompt:str
)->str:
    """
    Generate music from user description.

    User only waits for final music result.
    """

>>>>>>> Stashed changes
    os.makedirs(
        "outputs",
        exist_ok=True
    )
<<<<<<< Updated upstream
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
=======


    filename = (
        f"outputs/{uuid.uuid4()}.wav"
    )


    loop = asyncio.get_running_loop()


    future = loop.create_future()



    await music_queue.put(
        (
            prompt,
            filename,
            future
        )
    )


    print(
        f"📥 accepted: {prompt}"
    )


    # 等待自己的音乐
    result = await future


    return result




if __name__=="__main__":

>>>>>>> Stashed changes
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )