FROM centos:latest
MAINTAINER scs


RUN yum install python3 -y

COPY ./requirements.txt /requirement.txt

RUN pip3 install -r /requirement.txt
RUN mkdir /project
WORKDIR /project
COPY ./ /project

CMD python3 manage.py runserver 0.0.0.0:8000

EXPOSE 8000
