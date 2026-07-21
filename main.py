from music.music_generator import MusicGenerator
import os
import datetime


generator = MusicGenerator()


def main():


    os.makedirs(
        "outputs",
        exist_ok=True
    )


    while True:


        prompt=input(
            "\n🎵 输入音乐描述(exit退出): "
        )


        if prompt=="exit":
            break



        filename=(
            datetime.datetime.now()
            .strftime(
                "outputs/music_%Y%m%d_%H%M%S.wav"
            )
        )


        print(
            "\n正在生成音乐..."
        )


        path=generator.generate(
            prompt,
            filename
        )


        print(
            f"""
生成完成:

{path}
"""
        )



if __name__=="__main__":
    main()