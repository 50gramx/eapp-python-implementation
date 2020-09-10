#!/bin/bash
pip install -r /opt/ethos/apps/service/eapp-identity/requirements.txt
source /opt/ethos/apps/service/eapp-identity/id.env
python3 /opt/ethos/apps/service/eapp-identity/src/server.py