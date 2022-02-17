#!/usr/bin/python

import concurrent.futures
import json

import openstack


def new_project(uuid):
    return {
        "name": project_map[uuid],
        "server_count": 0,
        "flavor_ram": 0,
        "flavor_vcpus": 0,
        "volume_count": 0,
        "volume_size": 0,
        "floating_ips": 0,
    }


stats = {}
project_map = {}

pool = concurrent.futures.ThreadPoolExecutor(max_workers=100)
futures = []

# Our OpenStack is slow. This script is designed to submit everything in
# parallel and then process results as they are returned.

vols = pool.submit(openstack.list_volumes)
servers = pool.submit(openstack.list_servers)
fips = pool.submit(openstack.list_floating_ips)
projects = pool.submit(openstack.list_projects)

for volume in vols.result():
    print("looking up volume", volume["Name"])
    futures.append(
        pool.submit(lambda vid: ("volume", openstack.get_volume(vid)), volume["ID"])
    )

for server in servers.result():
    print("looking up server", server["Name"])
    futures.append(
        pool.submit(lambda sid: ("server", openstack.get_server(sid)), server["ID"])
    )

for fip in fips.result():
    print("looking up floating ip", fip["Floating IP Address"])
    futures.append(
        pool.submit(lambda fid: ("fip", openstack.get_floating_ip(fid)), fip["ID"])
    )

for project in projects.result():
    project_map[project["ID"]] = project["Name"]

for future in concurrent.futures.as_completed(futures):
    rtype, rinfo = future.result()

    if rtype == "fip":
        pid = rinfo["project_id"]
        if pid not in stats:
            stats[pid] = new_project(pid)

        if rinfo["port_id"]:
            stats[pid]["floating_ips"] += 1
    elif rtype == "volume":
        pid = rinfo["os-vol-tenant-attr:tenant_id"]
        if pid not in stats:
            stats[pid] = new_project(pid)

        stats[pid]["volume_count"] += 1
        stats[pid]["volume_size"] += rinfo["size"]
    elif rtype == "server":
        pid = rinfo["project_id"]
        if pid not in stats:
            stats[pid] = new_project(pid)
        flavor_id = rinfo["flavor"].split("(")[1].split(")")[0]
        flavor = openstack.get_flavor(flavor_id)
        stats[pid]["server_count"] += 1
        stats[pid]["flavor_ram"] += flavor["ram"]
        stats[pid]["flavor_vcpus"] += flavor["vcpus"]

with open("stats.json", "w") as fd:
    json.dump(stats, fd, indent=2)
