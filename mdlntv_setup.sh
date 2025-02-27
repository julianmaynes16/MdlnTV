#!/bin/bash

export DISPLAY=:0

if [ ! -d "/.venv/" ]; then
  python -m venv .venv
fi

. .venv/bin/activate

python main.py $1 $2 $3



