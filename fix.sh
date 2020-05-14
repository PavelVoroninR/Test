#!/usr/bin/env sh
for i in a c e g h; do
    for j in b d f j k; do
        for k in 1 3 5 7 9; do
            for l in 2 4 6 8 0; do
                echo user_$i$j$k${l}:user_$i$j$k${l} | chpasswd
                chown -R user_$i$j$k${l}:FTP /home/user_$i$j$k$l/*
                chmod 555 /home/user_$i$j$k$l
            done
        done
    done
done