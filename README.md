# backup-mx
Simple postfix backup mailserver / Backup-MX server. Based on Alpine Linux.

## Description
This Docker container is designed to function as a backup MX server for your email system. When your primary mail server is unavailable due to outages or maintenance, this container ensures that incoming emails are received and queued by Postfix. It attempts to deliver these emails as soon as the primary server becomes available, using DNS lookups to identify the highest-priority MX server configured for your domain. It includes health check to ensure the Postfix service is running smoothly. This container is ideal for maintaining email continuity and ensuring that no messages are lost during primary mail server downtime.

## TL;DR

To run the container, do the following:
```
docker run --rm --name backup-mx -e "HOSTNAME=mx2.example.com -e DOMAINS=example.com,example2.com" -p 25:25 theknigge/backup-mx
```

## Configuration options

The following configuration options are available:
```
ENV vars
$HOSTNAME = Postfix myhostname
$DOMAINS = Domains for relaying
$ACCESS_CODE = This variable sets the access code required to access the web interface. (Default: changeme)
```

### `Accessing the Web Interface`

Open your web browser and navigate to http://<your-container-ip>:5000?access_code=<$ACCESS_CODE> to view the Postfix queue status and manage the mail queue.

## Security

Postfix will run the master proces as `root`, because that's how it's designed. Subprocesses will run under the `postfix` account which will use `UID:GID` of `100:101`. Webinterface is secured by the access_code env variable. 
