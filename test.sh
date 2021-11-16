#!/bin/bash

# docker run --rm -it \
# -v $(pwd)/advent-init.py:/app/advent.py \
# -v $(pwd)/secrets:/app/secrets \
# -v $(pwd)/templates:/app/templates \
# -v $(pwd)/requirements.txt:/app/requirements.txt \
# -v $(pwd)/test.sh:/app/test.sh \
# python:3.10 /app/test.sh

pip3 install -r /app/requirements.txt
python3 /app/advent.py -y 2020 -d 15 -v -i -s /tmp
bash

