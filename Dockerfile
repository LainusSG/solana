# app/Dockerfile

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY /app .
#RUN pip3 install -r requirements.txt
RUN pip3 install streamlit streamlit-webrtc opencv-python-headless streamlit-authenticator matplotlib fpdf kaleido plotly sqlalchemy datetime psycopg2-binary  requests-toolbelt==0.10.1 Pyrebase4==4.6.0 urllib3==1.26.15

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:80/_stcore/health



ENTRYPOINT ["streamlit", "run", "inicio.py", "--server.port=80", "--server.address=0.0.0.0"]
#RUN app/ssl-proxy-linux-amd64  -from 0.0.0.0:8100 -to 127.0.0.1:8501
