from scipy.io.wavfile import write

import torch
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.models import MultiBandDiffusion
from audiocraft.data.audio import audio_write

import argparse
import runpod

from contextlib import redirect_stdout, redirect_stderr
import io

USE_DIFFUSION_DECODER = True

if USE_DIFFUSION_DECODER:
    mbd = MultiBandDiffusion.get_mbd_musicgen()

MODELS = ['facebook/musicgen-small', 'facebook/musicgen-melody']

def make_music(model=MODELS[0], 
               text='modern upbeat eletronic lofi beats',
               duration=10,
               name='output',
               sample_rate=32000):
    audio_files = []
    model = MusicGen.get_pretrained(model)
    model.set_generation_params(duration=duration)

    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout):
        with redirect_stderr(stderr):
            output = model.generate(
                descriptions=[
                    text
                ],
                progress=True, return_tokens=True
            )
    if USE_DIFFUSION_DECODER:
        out_diffusion = mbd.tokens_to_wav(output[1])
        outputs = torch.cat([output[0], out_diffusion], dim=0)
        outputs = outputs.detach().cpu().float()
        for out in outputs:
            i = 1
            with open(f"./{name}-{i}.wav", "wb") as f:
                audio_write(f"./{name}-{i}.wav", out, sample_rate, strategy="loudness",
                        loudness_headroom_db=16, loudness_compressor=True, add_suffix=False)
                audio_files.append(f"{name}-{i}.wav")
            i += 1
    return audio_files

def handler(job):
    job_input = job["input"] # Access the input from the request.
  
    # Add your custom code here.
    return job_input["prompt"] + " converted to output."

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--input', type=str, default='{"input": {"prompt": "your prompt"}}')
    # args = parser.parse_args()
    runpod.serverless.start({ "handler": handler}) # Required.
