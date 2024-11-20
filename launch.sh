#!/bin/bash
#
#  /*************************************************************************
#  *
#  * AMIT KUMAR KHETAN CONFIDENTIAL
#  * __________________
#  *
#  *  [2017] - [2021] Amit Kumar Khetan
#  *  All Rights Reserved.
#  *
#  * NOTICE:  All information contained herein is, and remains
#  * the property of Amit Kumar Khetan and its suppliers,
#  * if any.  The intellectual and technical concepts contained
#  * herein are proprietary to Amit Kumar Khetan
#  * and its suppliers and may be covered by U.S. and Foreign Patents,
#  * patents in process, and are protected by trade secret or copyright law.
#  * Dissemination of this information or reproduction of this material
#  * is strictly forbidden unless prior written permission is obtained
#  * from Amit Kumar Khetan.
#  */
#


echo "Sourcing environment"
. /app/implementation.dev.env


# Function to update file permissions and start SSH port forwarding
start_port_forwarding() {
  # Update permissions of settings/openvpn to 600
  chmod 600 /app/src/community/gramx/collars/DC499999999/openvpn

  # Start SSH port forwarding with updated permissions
  ssh -i /app/src/community/gramx/collars/DC499999999/openvpn -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -N -L 16443:13.200.238.161:16443 ec2-user@13.200.238.161 -v &
  SSH_PID=$!
}

# Start port forwarding
start_port_forwarding

# Function to check if the port forwarding process is running
check_port_forwarding() {
  if ! kill -0 $SSH_PID > /dev/null 2>&1; then
    echo "Port forwarding process has stopped. Restarting..."
    start_port_forwarding
  fi
}


echo "Starting Server"
python3 /app/src/server.py

# Server process PID
SERVER_PID=$!

# Infinite loop to monitor the port forwarding process
while true; do
  check_port_forwarding
  sleep 10
done