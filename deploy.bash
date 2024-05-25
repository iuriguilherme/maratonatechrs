#!/bin/bash

## Este arquivo só serve para deploy no servidor de desenvolvimento, 
## este script só roda em bash no linux

SERVER="gg"

EXCLUDES=( \
'Pipfile.lock' \
'.git' \
'.env' \
'instance' \
'*egg-info' \
'venv' \
)

DIR='usr/lib/maratonatechrs/'

rsync -avvhSP \
--delete \
$(for EXCLUDE in ${EXCLUDES[@]}; \
do echo -n "--exclude=${EXCLUDE} "; \
done) \
./ \
${SERVER}:${DIR}
