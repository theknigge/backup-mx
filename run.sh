# https://github.com/bokysan/docker-postfix

TZ="Etc/GMT-2"
TZ_FILE="/usr/share/zoneinfo/$TZ"
if [ -f "$TZ_FILE" ]; then
    echo -e "‣ Setting container timezone to: $TZ"
    ln -snf "$TZ_FILE" /etc/localtime
    echo "$TZ" >/etc/timezone
else
    echo -e "‣ Cannot set timezone to: $TZ -- this timezone does not exist."
fi

# https://samhobbs.co.uk/2016/01/mx-backup-postfix-email-server
# Make and reown postfix folders
mkdir -p /var/spool/postfix/ && mkdir -p /var/spool/postfix/pid
chown root: /var/spool/postfix/
chown root: /var/spool/postfix/pid

# Disable SMTPUTF8, because libraries (ICU) are missing in alpine
postconf -e smtputf8_enable=no

# Update aliases database. It's not used, but postfix complains if the .db file is missing
postalias /etc/postfix/aliases

if [[ ! -z "$HOSTNAME" && ! -z "$DOMAINS" ]]; then
    echo -e "‣ Setting myhostname: $HOSTNAME"
    postconf -e myhostname=$HOSTNAME
    postconf -e myorigin=$HOSTNAME
    postconf -e mydestination=$HOSTNAME,localhost
    echo -e "‣ Setting relay_domains: $DOMAINS"
    postconf -e relay_domains=$DOMAINS
    postconf -e relayhost=
    postconf -e proxy_interfaces=$HOSTNAME
fi

# Increase the allowed header size, the default (102400) is quite smallish
postconf -e header_size_limit=4096000
postconf -e minimal_backoff_time=180s
postconf -e maximal_backoff_time=1800s
postconf -e queue_run_delay=300s
postconf -e bounce_queue_lifetime=5d
postconf -e maximal_queue_lifetime=5d

# Restriction lists
postconf -e smtpd_helo_required=yes
postconf -e smtpd_helo_restrictions="reject_invalid_hostname, reject_non_fqdn_hostname, reject_unknown_hostname, reject_rhsbl_helo dbl.spamhaus.org, permit"
postconf -e smtpd_etrn_restrictions=reject
postconf -e smtpd_client_restrictions="permit_mynetworks, reject_unknown_client_hostname, reject_unauth_pipelining, permit"
postconf -e smtpd_sender_restrictions="permit_mynetworks, reject_unknown_sender_domain"
postconf -e smtpd_recipient_restrictions="permit_mynetworks, reject_unauth_pipelining, reject_non_fqdn_sender, reject_non_fqdn_recipient, reject_rbl_client zen.spamhaus.org, reject_rhsbl_sender dbl.spamhaus.org, reject_rhsbl_recipient dbl.spamhaus.org"
postconf -e smtpd_helo_required=yes
postconf -e header_checks=regexp:/etc/postfix/header_checks
postconf -e content_filter=smtp-amavis:[127.0.0.1]:10024



# Start services
echo -e "‣ Starting: rsyslog, postfix"
exec supervisord -c /etc/supervisord.conf
