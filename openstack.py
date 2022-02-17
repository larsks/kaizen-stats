#!/usr/bin/python

import json
import subprocess

from functools import cache


def openstack(*args):
    """Run `openstack` CLI.

    Append `-f json` to whatever arguments we receive from the caller, and
    parse the returned JSON before returning a result."""

    cmd = ["openstack"]
    cmd.extend(args)
    cmd.extend(["-f", "json"])
    return json.loads(subprocess.check_output(cmd))


@cache
def get_project(uuid):
    """Return details about a single project"""
    return openstack("project", "show", uuid)


@cache
def get_flavor(uuid):
    """Return details about a single flavor"""
    return openstack("flavor", "show", uuid)


def list_servers():
    """Return a list of nova servers (aka "instances")"""
    return openstack("server", "list", "--all")


@cache
def get_server(uuid):
    """Return details about a single server"""
    return openstack("server", "show", uuid)


def list_volumes():
    """Return a list of cinder volumes"""
    return openstack("volume", "list", "--all")


@cache
def get_volume(uuid):
    """Return details about a single volume"""
    return openstack("volume", "show", uuid)
