#!/bin/bash

start=0
end=50

for ((i=start; i<=end; i++)); do
    tunctl
    ip=($i + 1)
    tap=$i
    ip_address="10.0.5.$ip"
    network_interface="tap$tap"
    sudo ip addr add "$ip_address" dev "$network_interface"
    echo "Added IP $ip_address to $network_interface"
done

