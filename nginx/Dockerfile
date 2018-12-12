FROM nginx:latest

RUN apt-get update && \
    apt-get update -y && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get install openssl && \
    rm -rf /var/lib/apt/lists/*


# Required for envsubst, however, this is already in the upstream Dockerfile
# but has suddenly become unavailable in the base image.
RUN apt-get install gettext-base

COPY default.conf /etc/nginx/conf.d/default.conf.template
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

EXPOSE 443

CMD /entrypoint.sh

