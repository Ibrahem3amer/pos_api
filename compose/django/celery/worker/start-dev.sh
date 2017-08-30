#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

celery -A cl_inn.taskapp worker -l INFO
