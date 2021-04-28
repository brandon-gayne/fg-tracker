FROM ubuntu
RUN apt update && \ 
    apt upgrade -y && \ 
    apt -y install python3 python3-pip sudo iputils-ping
RUN pip3 install bs4 discord_webhook requests
RUN pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
COPY . /app
ENTRYPOINT [ "python3", "app/bot.py" ]