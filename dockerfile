FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get install -y \
        git \
        python3 \
        python3-pip

WORKDIR /home

RUN git clone https://github.com/jennyweb/Demonstratoren.git

RUN cd Demonstratoren

RUN pip3 install -r requirements.txt

RUN cd Simulation

RUN python3 heatbalance.py
