# get base image
FROM alpine:3.9
# get FTP server and python3
RUN apk update && \
    apk add 'vsftpd=3.0.3-r6' && \
    apk add 'python3=3.6.9-r2' && \
    rm -rf /var/cache/apk/*

# Create anonymous directory
RUN mkdir -p /var/run/vsftpd/empty
# Create ftp config 
RUN printf "listen=YES\n\
anonymous_enable=YES\n\
anon_root=/home/anonymous\n\
anon_upload_enable=YES\n\
anon_mkdir_write_enable=YES\n\
no_anon_password=YES\n\
local_enable=YES\n\
write_enable=YES\n\
allow_writeable_chroot=YES\n\
chroot_local_user=YES\n\
secure_chroot_dir=/var/run/vsftpd/empty\n\
seccomp_sandbox=NO\n\
chown_uploads=YES\n\
chown_username=anonymous\n\
listen_port=9098\n" > /etc/vsftpd.conf

# create 625 users for this server
# Generate per user:
# 1 file with size 1KiB
# 1 file with size 2KiB
# 1 file with size 1MiB
# total 10*(625*1 + 625*2 + 625*1024) = 6.121397018432617 GiB

RUN addgroup FTP && adduser -G FTP -D -g '' anonymous
RUN mkdir /home/anonymous/www && mkdir /home/anonymous/logs && chown -R anonymous /home/anonymous/*
RUN mkdir /root/generator_scripts
RUN mkdir /root/monitoring_script
WORKDIR /root/generator_scripts
COPY gen_users.sh /root/generator_scripts/gen_users.sh
COPY file_gen.py /root/generator_scripts/gen_files.py
COPY fix.py /root/generator_scripts/fix.sh
WORKDIR /root/monitoring_script
COPY monitor_script.py /root/monitoring_script/monitor_script.py
WORKDIR /
RUN chmod +x /root/generator_scripts/*
RUN /root/generator_scripts/gen_users.sh
CMD sh -c 'nohup vsftpd > /dev/null 2>&1& ; python3 /root/monitoring_script/monitor_script.py'
