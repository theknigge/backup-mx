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

# Restriction lists
postconf -e smtpd_client_restrictions=
postconf -e smtpd_sender_restrictions=
postconf -e smtpd_helo_required=yes
postconf -e smtpd_recipient_restrictions=permit_mynetworks, reject_unauth_destination, reject_unauth_pipelining, reject_invalid_hostname, reject_non_fqdn_hostname
postconf -e smtpd_relay_restrictions=permit_mynetworks
postconf -e smtpd_data_restrictions=reject_unauth_pipelining
postconf -e smtpd_end_of_data_restrictions=check_policy_service,reject_unauth_pipelining
postconf -e smtpd_etrn_restrictions=reject

# Add the SpamAssassin service to master.cf
echo "spamassassin unix - n n - - pipe user=spamd argv=/usr/bin/spamc -f -e /usr/sbin/sendmail -oi -f \${sender} \${recipient}" >> /etc/postfix/master.cf

# Start services
echo -e "‣ Starting: rsyslog, postfix"
exec supervisord -c /etc/supervisord.conf
