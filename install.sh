#!/bin/sh

cd $(dirname $0)

# Install pyinotify
cd pyinotify
python setup.py install
cd ..

# Install mapzipd
cp mapzipd /etc/init.d/mapzipd
cp mapzipd.conf /etc/mapzipd.conf
