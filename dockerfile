FROM jenkins/jenkins:lts
USER root

# パッケージリストを更新し、python3, flake8, pytest, zipをインストール
RUN apt-get update && \
    apt-get install -y python3 python3-flake8 python3-pytest zip && \
    rm -rf /var/lib/apt/lists/*

# Jenkinsユーザーに戻す
USER jenkins