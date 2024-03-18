#!/bin/bash

uvicorn app:app --host 0.0.0.0 --port 8000 --reload --log-config logging_config.ini