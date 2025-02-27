#!/bin/bash

export DISPLAY=:0

if [ ! -d "/.venv/" ]; then
  python -m venv .venv
fi

export PATH=/.venv/bin:$PATH

