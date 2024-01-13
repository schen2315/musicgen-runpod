from scipy.io.wavfile import write

import torch
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.models import MultiBandDiffusion
from audiocraft.data.audio import audio_write

import argparse
from upload_to_s3 import upload_file
import os
from contextlib import redirect_stdout, redirect_stderr
import io

MODELS = ['facebook/musicgen-small', 'facebook/musicgen-melody']

USE_DIFFUSION_DECODER = True

if USE_DIFFUSION_DECODER:
    mbd = MultiBandDiffusion.get_mbd_musicgen()

print(f"Is CUDA available: {torch.cuda.is_available()}")

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
            out_name = f"{name}-{i}.wav" 
            with open(out_name, "wb") as f:
                audio_write(out_name, out, sample_rate, strategy="loudness",
                        loudness_headroom_db=16, loudness_compressor=True, add_suffix=False)
                audio_files.append(out_name)
            i += 1
    return audio_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default=MODELS[0])
    parser.add_argument('--text', type=str, default='modern upbeat eletronic lofi beats')
    parser.add_argument('--duration', type=int, default=10)
    parser.add_argument('--sample_rate', type=int, default=32000)
    parser.add_argument('--name', type=str, default='output')

    args = parser.parse_args()
    files = make_music(model=args.model,
                        text=args.text,
                        duration=args.duration,
                        name=args.name,
                        sample_rate=args.sample_rate)
    for file in files:
        print(file)
