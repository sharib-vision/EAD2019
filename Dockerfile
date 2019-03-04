FROM continuumio/miniconda3
MAINTAINER Sharib Ali<sharib.ali@eng.ox.ac.uk> 

RUN conda create -n env python=3.6 numpy
RUN echo "source activate env" > ~/.bashrc

RUN mkdir /output/
RUN mkdir /input/

RUN chmod 777 /output/
RUN chmod 777 /input/

ENV PATH /opt/conda/envs/env/bin:$PATH

RUN conda install -c jmcmurray json 
RUN conda install -c conda-forge unzip 
RUN pip install tifffile

# create user ead2019
RUN useradd --create-home -s /bin/bash ead2019
USER ead2019

RUN mkdir -p /home/ead2019/app 
WORKDIR /home/ead2019/app

# add all evaluation and groundTruth directories
COPY evaluation_EAD2019_allFiles evaluation_EAD2019_allFiles/ 
COPY groundTruths_EAD2019 groundTruths_EAD2019/

# add run script
COPY run_script.sh run_script.sh

RUN [ "/bin/bash", "-c", "source activate env"]

RUN mkdir /home/ead2019/input/
RUN mkdir /home/ead2019/output/

# uncomment this for testing
#COPY ead2019_testSubmission /input/ead2019_testSubmission

#COPY ead2019_testSubmission/detection_bbox /input/detection_bbox
#COPY ead2019_testSubmission/semantic_bbox /input/semantic_bbox
#COPY ead2019_testSubmission/semantic_masks /input/semantic_masks
#COPY ead2019_testSubmission/generalization_bbox /input/generalization_bbox


#ENTRYPOINT /bin/bash

ENTRYPOINT ["bash"]
CMD ["/home/ead2019/app/run_script.sh"]


# docker run --mount source=ead2019_testSubmission.zip,target=/input -ti --rm  ead2019_v2:latest /bin/bash
