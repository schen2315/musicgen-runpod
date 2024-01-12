from melody import load_diffusion_decoder
from melody import make_music
from upload_to_s3 import upload_files

import runpod

import os

BUCKET = os.environ['BUCKET']
REGION = os.environ.get('REGION', 'us-east-1')

def handler(job):
    job_input = job["input"] # Access the input from the request.
  
    # Add your custom code here.
    return job_input["prompt"] + " converted to output."

if __name__ == "__main__":
    runpod.serverless.start({ "handler": handler}) # Required.
