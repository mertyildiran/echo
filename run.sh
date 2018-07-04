#!/bin/bash

redis-server &
python3 manage.py runserver &
celery -A echo worker -l info &
celery -A echo beat -l info
