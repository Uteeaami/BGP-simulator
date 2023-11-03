#!/bin/bash

start=0
end=50

for ((i=start; i<=end; i++)); do
    ip=($i + 1)
    tap=$i
    ip_address="10.0.5.$ip"
    network_interface="tap$tap"

    if [ "$DOCKER_ENV" = "true" ]; then
        # Running in Docker, don't use sudo
        ip addr del "$ip_address" dev "$network_interface"
        ip link delete "$network_interface" type veth
    else
        # Running in development, use sudo
        sudo ip addr del "$ip_address" dev "$network_interface"
        sudo ip link delete "$network_interface" type veth
    fi

    echo "Removed IP $ip_address from $network_interface"
    echo "Deleted network interface $network_interface"
done
