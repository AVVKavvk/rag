#!/bin/bash

python -m uvicorn app.core.main:app --host 0.0.0.0 --port 9991 --reload