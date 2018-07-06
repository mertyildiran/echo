# echo

the RESTful API of echo: voice-focused dating app, written on top of Django REST framework

<p align="center">
  <img src="https://i.imgur.com/BXRSW6g.png" alt="App icon" height="300px"/>
</p>

### Installation

We assume that you have Python 3.6.5, pip, Redis, GDAL library and libspatialite (or PostGIS) installed on your environment. If these requirements are satisfied then run:

```Shell
pip3 install -r requirements.txt
```

### Usage

This script will start a Redis Server, the Django RESTful API and Celery Periodic Tasks:

```Shell
./run.sh
```
