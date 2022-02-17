#!/usr/bin/python

import concurrent.futures
import json
import subprocess

from functools import cache
from collections import defaultdict


def openstack(*args):
    cmd = ["openstack"]
    cmd.extend(args)
    cmd.extend(["-f", "json"])
    return json.loads(subprocess.check_output(cmd))


@cache
def get_project(uuid):
    return openstack("project", "show", uuid)


@cache
def get_flavor(uuid):
    return openstack("flavor", "show", uuid)


def list_servers():
    return openstack("server", "list", "--all")


@cache
def get_server(uuid):
    return openstack("server", "show", uuid)


def list_volumes():
    return openstack("volume", "list", "--all")


@cache
def get_volume(uuid):
    return openstack("volume", "show", uuid)
