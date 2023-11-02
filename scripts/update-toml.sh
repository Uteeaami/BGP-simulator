#!/bin/bash


num_interfaces=50


echo "real_address = [" > new_config.toml


for ((i=0; i<=num_interfaces; i++)); do
  interface="tap${i}"
  inet_info=$(ifconfig "$interface" | awk '/inet / {print $2}')
  if [ -n "$inet_info" ]; then
    echo "\"$inet_info\"," >> new_config.toml
  fi
done


echo "]" >> new_config.toml
echo "connections = [["\"r1\"", "\"r2\""], [\"r1\", \"r3\"], [\"r2\", \"r4\"], [\"r3\", \"r6\"], [\"r5\", \"r6\"], [\"r6\", \"r8\"], [\"r7\", \"r1\"], [\"r9\", \"r4\"], [\"r10\", \"r5\"]]" >> new_config.toml


mv new_config.toml ../config.toml

echo "New config.toml file created with updated IP addresses and static connections."
