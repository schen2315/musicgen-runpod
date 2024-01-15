from melody import make_music
from upload_to_s3 import upload_files

import runpod

import os

OUTPUTS_DIR = './outputs'

def handler(job):
    job_input = job["input"] # Access the input from the request.
    
    s3_creds = job["s3Config"]

    # Add your custom code here.
    print(f"Using prompt={job_input['prompt']}")
    print(f"Using name={job_input['name']}")
    audio_files = make_music(text=job_input["prompt"], name=f"{OUTPUTS_DIR}/{job_input['name']}")
    # save to s3
    upload_files(audio_files, s3_creds["bucketName"], aws_access_key_id=s3_creds["accessId"], aws_secret_access_key=s3_creds["accessSecret"])
    return job_input['prompt'] + " converted to output."

if __name__ == "__main__":
    runpod.serverless.start({ "handler": handler}) # Required.
