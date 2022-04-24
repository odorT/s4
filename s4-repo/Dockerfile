FROM python:3.9

COPY . .

### WARNING
## REMOVE FOLLOWING LINE WHEN DEPLOYING TO PRODUCTION
COPY key.json /home/key.json

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DEBUG True
ENV SECRET_KEY S3cr3t_K#Key
ENV DB_ENGINE postgresql
ENV DB_NAME s4-flask
ENV DB_HOST localhost
ENV DB_PORT 5432
ENV DB_USERNAME s4-flask-user
ENV DB_PASS mysecretpassword

# install python dependencies
RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-pgsql.txt

RUN apt-get update && \
    apt-get install -y curl gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && \
    apt-get update -y && \
    apt-get install google-cloud-sdk -y

RUN gcloud auth activate-service-account s4-310@vital-wavelet-346108.iam.gserviceaccount.com  --key-file=/home/key.json --project=vital-wavelet-346108

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
