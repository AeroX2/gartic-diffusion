FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime as python-base
WORKDIR /workdir
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY setup.py .
ENV HF_HOME /opt/hf
RUN --mount=type=cache,target=/opt/hf python3 setup.py

COPY src /workdir/src
WORKDIR /workdir/src

CMD ["/bin/sh", "-c", "rq worker --with-scheduler --url ${REDIS_URL}"]
EXPOSE 5000