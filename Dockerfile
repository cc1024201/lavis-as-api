FROM ubuntu

WORKDIR /image-captioner-api

COPY requirements.txt /image-captioner-api/requirements.txt

RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3 -y
RUN python3 --version
RUN apt install python3-pip -y
RUN pip install --upgrade pip
RUN pip install --ignore-installed blinker==1.5
RUN pip install --no-cache-dir --upgrade -r /image-captioner-api/requirements.txt

COPY . /image-captioner-api/src

WORKDIR /image-captioner-api/src

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
