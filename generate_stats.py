#!/usr/bin/python

import concurrent.futures
import json

import openstack


def new_project(uuid):
    p = openstack.get_project(uuid)
    return {
        "name": p["name"],
        "server_count": 0,
        "flavor_ram": 0,
        "flavor_vcpus": 0,
        "volume_count": 0,
        "volume_size": 0,
    }


projects = {}

pool = concurrent.futures.ThreadPoolExecutor(max_workers=100)
futures = []
for volume in openstack.list_volumes():
    print("looking up volume", volume["Name"])
    futures.append(pool.submit(openstack.get_volume, volume["ID"]))

for future in concurrent.futures.as_completed(futures):
    v = future.result()
    print("processing volume", v["name"])
    project = v["os-vol-tenant-attr:tenant_id"]

    if project not in projects:
        projects[project] = new_project(project)

    projects[project]["volume_count"] += 1
    projects[project]["volume_size"] += v["size"]

futures = []
for server in openstack.list_servers():
    print("looking up server", server["Name"])
    futures.append(pool.submit(openstack.get_server, server["ID"]))

for future in concurrent.futures.as_completed(futures):
    s = future.result()
    print("processing server", s["name"])
    project = s["project_id"]

    if project not in projects:
        projects[project] = new_project(project)

    flavor_id = s["flavor"].split("(")[1].split(")")[0]
    flavor = openstack.get_flavor(flavor_id)
    projects[project]["server_count"] += 1
    projects[project]["flavor_ram"] += flavor["ram"]
    projects[project]["flavor_vcpus"] += flavor["vcpus"]


with open("stats.json", "w") as fd:
    json.dump(projects, fd, indent=2)
