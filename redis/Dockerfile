ARG GCC_VERSION=11

FROM gcc:${GCC_VERSION} AS builder

ARG REDIS_VERSION=7.0.9


RUN wget https://download.redis.io/releases/redis-${REDIS_VERSION}.tar.gz && \
    tar xvzf redis-${REDIS_VERSION}.tar.gz && \
    cd redis-${REDIS_VERSION} && \
    make CFLAGS="-static" EXEEXT="-static" LDFLAGS="-static" && \
    mkdir -p /output/bin

WORKDIR /output/bin
RUN cp /redis-${REDIS_VERSION}/src/redis-server .


RUN mkdir -p /output/conf
WORKDIR /output/conf
RUN cp /redis-${REDIS_VERSION}/redis.conf .

FROM scratch

COPY --from=builder /output/conf/redis.conf /etc/redis/redis.conf
COPY --from=builder /output/bin/*           /bin/

ENTRYPOINT ["/bin/redis-server", "/etc/redis/redis.conf"]
