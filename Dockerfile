FROM alpine

RUN apk add --update --no-cache postfix postfix-pcre ca-certificates tzdata supervisor rsyslog spamassassin spamass-milter

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
