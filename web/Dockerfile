FROM node:lts-alpine

# HTTP server for serving static content
RUN npm install -g http-server -verbose

RUN apk add g++ make python 

WORKDIR /web

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build:pro

EXPOSE 443
CMD [ "http-server", "--ssl", "--cert", "pp-apicpl-1-mad.hi.inet.pem", "dist" ]

