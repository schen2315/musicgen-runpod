from ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir /workdir
WORKDIR /workdir

RUN apt-get update && \
    apt-get -y install ffmpeg
    
RUN apt-get -y install python3.10
RUN apt-get -y install python3-pip
RUN apt-get -y install python3.10-venv

#RUN python3.10 -m venv venv && \
#    . venv/bin/activate && pip install --upgrade pip
RUN pip3.10 install 'torch==2.1.0' setuptools wheel
RUN pip3.10 install xformers
RUN pip3.10 install runpod
RUN pip3.10 install -U audiocraft
RUN pip3.10 install -U scipy

RUN apt-get -y install git
RUN git clone https://github.com/schen2315/musicgen-api


# ADD ./test_handler.py .
# ADD ./test_input.json .
ADD handler.py .

# CMD ["python", "-u", "test_handler.py"]
CMD ["/bin/sh", "-c", "sleep", "infinity"]
