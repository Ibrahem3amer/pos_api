#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

rm -f './celerybeat.pid'
celery -A cl_inn.taskapp beat -l INFO
