FROM oven/bun:1-slim AS builder
WORKDIR /usr/src/app
COPY package.json .
COPY bun.lock* .
RUN bun i --frozen-lockfile

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
