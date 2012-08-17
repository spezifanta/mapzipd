#!/bin/sh

BASE=$(dirname $0)

# Install pyinotify
cd $BASE
cd pyinotify
python setup.py install

# Install mapzipd
cd $BASE
cp mapzipd /etc/init.d/mapzipd
cp mapzipd.conf /etc/mapzipd.conf
