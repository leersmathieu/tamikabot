FROM node

COPY . /opt/app
WORKDIR /opt/app

CMD npm start