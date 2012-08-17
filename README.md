# Map Zip Daemon

Automatically zips maps and moves them to a public web directory whenever a new map is uploaded to the game server's map directory.
Supports multiple game server sessions.

* License: MIT


## Dependencies

* Linux ≥ 2.6.13
* Python ≥ 2.5


## Install

    $ git clone https://github.com/spezifanta/mapzipd.git
    $ cd mapzipd
    $ git submodule init
    $ git submoule update
    $ sudo ./install.sh

To start, restart and stop mapzipd use

    $ sudo service mapzipd {start,stop,restart}


## Config

Open `/etc/mapzipd.conf` for settings. After changing settings a restart of mapzipd is required:
`sudo service mapzipd restart`

### Web direcory

Set `webdir` equal to your `sv_downloadurl` value in your `server.cfg`.

### Game server

Add each game server in a sperate line by using it's full path to it's root directory (one above the `maps` directory).

Example:
If your maps are strored at `/home/myaccount/orangebox/tf/maps` you will only add `/home/myaccount/orangebox/tf`

