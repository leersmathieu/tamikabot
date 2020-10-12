FROM node:alpine
RUN apk add  --no-cache ffmpeg

WORKDIR /opt/app

COPY package*.json ./
COPY . /opt/app
RUN npm install
RUN npm audit fix

CMD npm start