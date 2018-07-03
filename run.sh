#!/bin/bash

nohup redis-server &> redis.out&
nohup python3 manage.py runserver &> django.out&
nohup celery -A echo worker -l info &> celery-worker.out&
nohup celery -A echo beat -l info &> celery-beat.out&
