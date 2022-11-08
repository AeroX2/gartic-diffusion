FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime as runtime
WORKDIR /workdir
RUN apt-get update
RUN apt-get install -y git git-lfs

RUN git lfs install
RUN git clone -b fp16 https://GarticDiffusion:4QFAURzCghfkQnJ@huggingface.co/runwayml/stable-diffusion-v1-5/

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY src /workdir/src
WORKDIR /workdir/src

CMD ["/bin/sh", "-c", "rq worker --with-scheduler --url ${REDIS_URL}"]
EXPOSE 5000
