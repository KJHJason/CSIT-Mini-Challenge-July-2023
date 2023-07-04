FROM python:3.11.4-slim

# Copy local code to the container image
ENV APP_HOME /api
COPY /src $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN pip install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["python3", "main.py"]
