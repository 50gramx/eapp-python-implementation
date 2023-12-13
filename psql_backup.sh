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

echo "Postgres Backup Initiated"
BACKUP_DIR="/backups"
BACKUP_FILE="$BACKUP_DIR/backup_$(date +\%Y\%m\%d_%H%M%S_%Z).sql"

# Perform a backup
perform_backup() {
    pg_dump -U user -d mydatabase --file=$BACKUP_FILE
    echo "Postgres Dumped $BACKUP_FILE"
}

if [ "$1" = "instant" ]; then
    # Triggered manually or by another container
    perform_backup
elif [ "$1" = "wait_for_stop_signal" ]; then
    # Triggered by container stop signal
    # Trap SIGINT signal and invoke the backup function
    trap 'perform_backup' SIGINT
    # Keep the script running
    echo "Stop listener script is running. Press Ctrl+C to stop."
    sleep infinity
else
    # Scheduled backup
    perform_backup
fi