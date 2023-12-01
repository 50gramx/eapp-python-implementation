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
CONTAINER_NAME="eapp-python-implementation-postgres-1"
BACKUP_DIR="/backups"
BACKUP_FILE="$BACKUP_DIR/backup_$(date +\%Y\%m\%d_%H%M%S_%Z).sql"

PG_CONFIG_FILE="/custom_postgresql.conf"

docker exec -t $CONTAINER_NAME pg_dump -U user -d mydatabase --file=$BACKUP_FILE --config=$PG_CONFIG_FILE
echo "Postgres Dumped $BACKUP_FILE"

echo "0 0 * * * /psql_backup.sh" > /etc/crontabs/root
echo "Postgres Cron Activated 0 0 * * * "