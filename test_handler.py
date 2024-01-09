# your_handler.py

import runpod # Required.

def handler(job):
  job_input = job["input"] # Access the input from the request.
  
  # Add your custom code here.

  return job_input["prompt"] + " converted to output."

runpod.serverless.start({ "handler": handler}) # Required.
