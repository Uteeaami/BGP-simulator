#!/bin/bash

start=0
end=20

for ((i=start; i<=end; i++)); do
    ip=($i + 1)
    tap=$i
    ip_address="10.0.5.$ip"
    network_interface="tap$tap"
    sudo ip addr del "$ip_address" dev "$network_interface"
    echo "Removed IP $ip_address from $network_interface"
    sudo ip link delete "$network_interface" type veth
    echo "Deleted network interface $network_interface"
done
