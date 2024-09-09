#!/bin/sh

socat TCP-L:1305,reuseaddr,fork EXEC:"python3 server.py"
