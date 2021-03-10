#!/bin/bash
pip install -r /opt/ethos/apps/service/eapp-identity/requirements.txt
source /opt/ethos/wiki/eapp-wiki/config/environment/microservices/eapp-identity.local.env
python3 /opt/ethos/apps/service/eapp-identity/src/server.py