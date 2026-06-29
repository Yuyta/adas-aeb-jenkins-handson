FROM jenkins/jenkins:lts

USER root

# Python、pip、zipをインストール
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        zip && \
    rm -rf /var/lib/apt/lists/*

# flake8 と pytest を pip でインストール
RUN pip3 install --break-system-packages \
        flake8 \
        pytest

USER jenkins