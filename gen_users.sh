#!/usr/bin/env sh
RANDOM_SEED=42
# if ["$1" != ""]
# then
#     RANDOM_SEED=$1
# fi
for i in a c e g h; do
    for j in b d f j k; do
        for k in 1 3 5 7 9; do
            for l in 2 4 6 8 0; do
                adduser -D -g '' -G FTP user_$i$j$k$l 
                echo \"user_$i$j$k$l:user_$i$j$k$l\" | chpasswd > /dev/null 2>&1 
                mkdir /home/user_$i$j$k$l/www > /dev/null 2>&1
                mkdir /home/user_$i$j$k$l/logs > /dev/null 2>&1
                for m in 1 2 3 4 5 6 7 8 9 0; do
                    python3 /root/generator_scripts/gen_files.py -l 1024 -n /home/user_$i$j$k$l/logs/$i$j${m}_log.log -s $RANDOM_SEED
                    python3 /root/generator_scripts/gen_files.py -l 2048 -n /home/user_$i$j$k$l/logs/$j$l${m}_log.log -s $RANDOM_SEED
                    python3 /root/generator_scripts/gen_files.py -l 1048576 -n /home/user_$i$j$k$l/logs/$l$k${m}_log.log -s $RANDOM_SEED
                done
                chown -R user_$i$j$k${l}:FTP /home/user_$i$j$k$l/* > /dev/null 2>&1
                chmod 555 /home/user_$i$j$k${l} > /dev/null 2>&1
            done
        done
    done
done