FROM nvidia/cuda:12.2.0-devel-ubuntu20.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#Install libs
RUN apt-get update --fix-missing && apt-get install -y \
			g++ \
			build-essential \
			cmake \			
			pkg-config \
			python3-dev \
			python3-pip \
			nano \
            libgl1-mesa-glx \
            libglib2.0-0 \
            vim
RUN apt-get install -y libenchant1c2a

# Language and timezone

# Install packages
RUN pip3 install --upgrade pip
RUN pip3 install torch==2.1.1
RUN pip3 install requests flask flask_cors flask_restplus Werkzeug==0.16.0 gunicorn eventlet pyjwt pymongo
RUN pip3 install fuzzywuzzy python-Levenshtein nltk==3.6.1 scikit-learn==0.24.0 scikit-image unidecode
RUN apt-get install -y libzbar0
RUN pip3 install python-logstash libgen-api
RUN pip3 install opencv-python opencv-contrib-python imutils
RUN pip3 install markupsafe==2.0.1 flask==1.1.4 
RUN pip3 install pandas google-cloud-vision
RUN pip3 install pyenchant
RUN pip3 install pyvi pdfplumber flask_restx
RUN pip3 install accelerate
RUN pip3 install bitsandbytes
RUN pip3 install transformers==4.32.0 accelerate tiktoken einops scipy transformers_stream_generator==0.0.4 peft deepspeed
RUN pip3 install sentence_transformers
RUN pip3 install faiss-cpu
RUN pip3 install pyvi
RUN pip3 install numpy
RUN pip3 install jupyterlab
RUN pip3 install scipy
# Add
ADD . /code/
WORKDIR /code/
