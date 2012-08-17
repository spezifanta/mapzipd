#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import os
import shlex
import subprocess
import time
import unittest

class MapZipDaemonWatchTestCase(unittest.TestCase):
    def setUp(self):
        setup()
    
    def test_watchdog(self):
        # Check if setup worked correct
        self.assertTrue(os.path.exists('/tmp/webdir/fastdownload/maps'))
        self.assertTrue(os.path.exists('/tmp/gameserver_0/maps'))
        self.assertTrue(os.path.exists('/tmp/gameserver_1/maps'))
        self.assertTrue(os.path.exists('/tmp/gameserver_2/maps'))
        self.assertTrue(os.path.exists('/tmp/gameserver_0/maps/fake_map_0.bsp'))
        self.assertTrue(os.path.exists('/tmp/gameserver_1/maps/fake_map_1.bsp'))
        self.assertTrue(os.path.exists('/tmp/gameserver_2/maps/fake_map_2.bsp'))

        # There should be no maps
        self.assertFalse(os.path.exists('/tmp/webdir/fastdownload/maps/fake_map_0.bsp.bz2'))
        self.assertFalse(os.path.exists('/tmp/webdir/fastdownload/maps/fake_map_1.bsp.bz2'))
        self.assertFalse(os.path.exists('/tmp/webdir/fastdownload/maps/fake_map_2.bsp.bz2'))

        # Fake a map copy        
        subprocess.call(shlex.split('touch /tmp/gameserver_0/maps/fake_map_0.bsp'))
        subprocess.call(shlex.split('touch /tmp/gameserver_1/maps/fake_map_1.bsp'))
        subprocess.call(shlex.split('touch /tmp/gameserver_2/maps/fake_map_2.bsp'))

        # Wait until the maps got copied
        time.sleep(1)

        # Now there should be some maps
        self.assertTrue(os.path.exists('/tmp/webdir/fastdownload/maps/fake_map_0.bsp.bz2'))
        self.assertTrue(os.path.exists('/tmp/webdir/fastdownload/maps/fake_map_1.bsp.bz2'))
        self.assertTrue(os.path.exists('/tmp/webdir/fastdownload/maps/fake_map_2.bsp.bz2'))

    def test_ownership(self):
        # Check setup
        self.assertTrue(os.path.exists('/tmp/webdir/fastdownload/maps'))
        self.assertTrue(os.path.exists('/tmp/gameserver_0/maps'))

        # Fake webdir's ownershop and verify        
        default_owner = 1000 # default on most *unix systems
        os.chown('/tmp/webdir/fastdownload/maps', default_owner, default_owner)

        self.assertEqual(os.stat('/tmp/webdir/fastdownload/maps').st_uid, default_owner)
        self.assertEqual(os.stat('/tmp/webdir/fastdownload/maps').st_gid, default_owner)

        # 'Copy' a new map into the gameserver dir
        create_fake_map('/tmp/gameserver_0/maps/foobar.bsp')

        # Wait until map got copied
        time.sleep(1)

        # Verify our new ownership
        self.assertEqual(os.stat('/tmp/webdir/fastdownload/maps/foobar.bsp.bz2').st_uid, default_owner)
        self.assertEqual(os.stat('/tmp/webdir/fastdownload/maps/foobar.bsp.bz2').st_gid, default_owner)

    def tearDown(self):
        cleanup()


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def rmdir(dir):
    if not os.path.exists(dir):
        return

    for item in os.listdir(dir):
        file_path = os.path.join(dir, item)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            rmdir(file_path)
    
    os.rmdir(dir)

def create_fake_map(name):
    bsp_file = file(name, 'w')
    bsp_file.write('VBSP')
    bsp_file.close()

def setup():
    # Create fake environment
    mkdir('/tmp/webdir/fastdownload/maps')

    for i in xrange(0, 3):
        mkdir('/tmp/gameserver_%d/maps' % i)
        create_fake_map('/tmp/gameserver_%d/maps/fake_map_%d.bsp' % (i, i))

    # Start mapzipd using custom config
    subprocess.call(shlex.split('../mapzipd start --config=mapzipd.conf'))

def cleanup():
    subprocess.call(shlex.split('../mapzipd stop --config=mapzipd.conf'))

    rmdir('/tmp/gameserver_0')
    rmdir('/tmp/gameserver_1')
    rmdir('/tmp/gameserver_2')
    rmdir('/tmp/webdir')

if __name__ == '__main__':
    unittest.main()
