FROM node:12.18.4
MAINTAINER Gunter Mingato

ARG VERSION

RUN git config --global http.sslVerify false
RUN git clone "https://Gunter:b1i2t3@git.webmodule.com.br/scm/wmser/socket.git"
WORKDIR /socket

COPY . .

RUN npm install

RUN npm install -g nodemon
RUN npm install --save express
RUN npm install --save jwt-decode

ENTRYPOINT ["npm", "start"]
EXPOSE 30000 30001