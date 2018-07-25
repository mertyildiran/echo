# echo

the RESTful API of echo: voice-focused dating app, written on top of Django REST framework

<p align="center">
  <img src="https://i.imgur.com/BXRSW6g.png" alt="App icon" height="200px"/>
</p>

<p align="center">
  <img src="https://i.imgur.com/mdCa8I2.jpg" alt="Feature graphic" height="300px"/>
</p>

#### Android Client

<a href="https://play.google.com/store/apps/details?id=computer.dragon.echo&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1"><img alt="Get it on Google Play" src="https://play.google.com/intl/en_us/badges/images/generic/en_badge_web_generic.png" height="100px" /></a>

### Installation

Make sure your Python version is 3.6.5 and pip3 installed on your system. To install Redis, GDAL library, libspatialite (or PostGIS) and the other dependencies run:

```Shell
sudo ./install.sh
pip3 install -r requirements.txt
```

### Usage

This script will start a Redis Server, the Django RESTful API and Celery Periodic Tasks:

```Shell
python3 manage.py migrate
./run.sh
```
