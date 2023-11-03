#!/bin/bash

start=0
end=50

for ((i=start; i<=end; i++)); do
    tunctl
    ip=($i + 1)
    tap=$i
    ip_address="10.0.5.$ip"
    network_interface="tap$tap"

    if [ "$DOCKER_ENV" = "true" ]; then
        # Running in Docker, don't use sudo
        ip addr add "$ip_address" dev "$network_interface"
    else
        # Running in development, use sudo
        sudo ip addr add "$ip_address" dev "$network_interface"
    fi

    echo "Added IP $ip_address to $network_interface"
done

