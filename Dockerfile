FROM alpine

# Install necessary packages one by one
RUN apk update && \
    apk add --no-cache postfix && \
    apk add --no-cache postfix-pcre && \
    apk add --no-cache ca-certificates && \
    apk add --no-cache tzdata && \
    apk add --no-cache supervisor && \
    apk add --no-cache rsyslog && \
    apk add --no-cache python3 && \
    apk add --no-cache py3-pip

# Install Flask
RUN pip3 install Flask

# Copy the code
COPY server.py /app/server.py
COPY supervisord.conf /etc/supervisord.conf
COPY rsyslog.conf /etc/rsyslog.conf
COPY run.sh /

RUN chmod +x /run.sh

# Expose necessary ports
EXPOSE 25 587 5000

USER root

CMD ["/bin/sh", "-c", "/run.sh"]
