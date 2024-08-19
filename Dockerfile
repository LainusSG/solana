# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/cashogomez/soldadura.git .

RUN pip3 install -r solana.txt
RUN pip install streamlit streamlit-webrtc opencv-python-headless streamlit-authenticator matplotlib

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health



ENTRYPOINT ["streamlit", "run", "inicio.py", "--server.port=8501", "--server.address=0.0.0.0"]
#RUN app/ssl-proxy-linux-amd64  -from 0.0.0.0:8100 -to 127.0.0.1:8501