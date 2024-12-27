#!/bin/bash

# Variables
WORKERS=1               
PORT=80               
HOST=0.0.0.0             



exec uvicorn src.main:app \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    --log-level info\
    --reload

