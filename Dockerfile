FROM linuxserver/ffmpeg
RUN apt update --yes
RUN apt install -y wget unzip
RUN mkdir -p /root/.cache/vosk 

RUN cd /root/.cache/vosk && wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip && unzip vosk-model-small-ru-0.22.zip
RUN apt install --yes software-properties-common
RUN apt install --yes python3 && apt install -y python3-pip

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
