# Compile and install Redis
apt-get update
apt-get install build-essential tcl

cd /tmp
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install

# GDAL library
apt-get install gdal-bin python-gdal
apt-get install --reinstall libspatialite7
apt-get install libsqlite3-mod-spatialite
