FROM node:16-alpine
WORKDIR /vue
COPY package.json .
COPY ./node_modules ./node_modules
COPY . .
RUN npm run build
