FROM python:3.8-slim
RUN apt-get update && apt-get install git -y
WORKDIR /srv/slack_bot
COPY . .
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD [ "flask", "run", "--host=0.0.0.0"]