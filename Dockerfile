FROM node:22-slim AS builder

# install git to install plugins
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY package.json .
COPY package-lock.json* .
COPY .npmrc* .
COPY quartz/ ./quartz/
COPY quartz.lock.json* .
RUN npm install; npx quartz plugin install

FROM oven/bun:1-slim
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/ /usr/src/app/
COPY . .
EXPOSE 8080
RUN groupadd -g 1001 1001 && useradd -M -s /bin/bash -g 1001 -u 1001 1001
RUN chown -R 1001:1001 /usr/src/app
USER 1001
# RUN chmod -R u+rw /usr/src/app
CMD ["bun", "run", "-b", "/usr/src/app/quartz/bootstrap-cli.mjs", "build", "--serve"]
