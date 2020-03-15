# pull official base image
FROM python:3.6

# set work directory
WORKDIR /server

# copy project file to workdir
COPY . .

# go to project dir and install dependencies
RUN cd /server && pip install -r requirements.txt

EXPOSE 80

CMD [ "python3" ,"/server/server.py"]
