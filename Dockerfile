FROM node:12

WORKDIR /opt/app

COPY package*.json ./
COPY . /opt/app

RUN apk add  --no-cache ffmpeg
RUN npm install
RUN npm audit fix

CMD npm start