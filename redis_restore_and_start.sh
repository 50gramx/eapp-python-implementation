#!/bin/sh

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

echo "Redis Restore Initiated"
# Restore the latest backup
LATEST_BACKUP=$(ls -t /backups/backup_*.rdb | head -n 1)
cp $LATEST_BACKUP /data/dump.rdb
echo "Redis Copied $LATEST_BACKUP"

# Start Redis server
echo "Redis Start Server"
exec redis-server