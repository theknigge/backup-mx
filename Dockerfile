FROM alpine:latest

# Install necessary packages one by one
RUN apk update && \
    apk add --no-cache postfix && \
    apk add --no-cache postfix-pcre && \
    apk add --no-cache ca-certificates && \
    apk add --no-cache tzdata && \
    apk add --no-cache supervisor && \
    apk add --no-cache rsyslog && \
    apk add --no-cache spamassassin
RUN sed -i 's/ENABLED=0/ENABLED=1/' /etc/default/spamassassin && \
    sed -i 's/CRON=0/CRON=1/' /etc/default/spamassassin


COPY supervisord.conf /etc/supervisord.conf
COPY rsyslog.conf /etc/rsyslog.conf
COPY run.sh /

RUN chmod +x /run.sh

# Expose necessary ports
EXPOSE 25 587

USER root

CMD ["/bin/sh", "-c", "/run.sh"]
