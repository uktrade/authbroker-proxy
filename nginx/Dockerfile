FROM nginx:latest

RUN apt-get update && apt-get install openssl

COPY default.conf /etc/nginx/conf.d/default.conf.template
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

EXPOSE 443

CMD /entrypoint.sh

