import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile

import threading
gpu_lock = threading.Lock()

class MusicGenerator:
    def __init__(self):
        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )
        print(f"Using device: {self.device}")
        model_id = ("facebook/musicgen-small")
        self.processor = (
            AutoProcessor.from_pretrained(
                model_id
            )
        )
        self.model = (
            MusicgenForConditionalGeneration
            .from_pretrained(
                model_id,
                torch_dtype=torch.float16
                if self.device=="cuda"
                else torch.float32
            )
            .to(self.device)
        )
    def generate(
        self,
        prompt:str,
        output:str
    ):
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        )
        inputs = {
            k:v.to(self.device)
            for k,v in inputs.items()
        }
        with gpu_lock:
            print("prepare inputs")
            print("start generate")
            audio_values = (
                self.model.generate(
                    **inputs,
                    max_new_tokens=512
                )
            )
            print("finish generate")
        sampling_rate = (
            self.model.config.audio_encoder.sampling_rate
        )
        audio = (
            audio_values[0]
            .cpu()
            .numpy()
            .astype("float32")
            .squeeze()
        )
        scipy.io.wavfile.write(
            output,
            rate=sampling_rate,
            data=audio
        )
        return output