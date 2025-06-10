FROM python:3.10-alpine
LABEL maintainer="Egemen Yavuz <melih.egemen.yavuz@elvia.no>"

COPY ./service /service
WORKDIR /service

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000/tcp
ENTRYPOINT ["python"]
CMD ["service.py"]
