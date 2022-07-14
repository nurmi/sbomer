#!/usr/bin/env python3

import requests
import sys
import json

url = "https://hub.docker.com/v2/repositories/library/?page=1&page_size=15"

output = { "containers": [] }

convert_map = {
    # these images do not publish a 'latest' tag
    "library/elasticsearch:latest": ["library/elasticsearch:8.3.2"],
    "library/kibana:latest": ["library/kibana:8.3.2"],
    "library/logstash:latest": ["library/logstash:8.3.2"],    
    "library/jenkins:latest": ["library/jenkins:2.60.3"],
    "library/oraclelinux:latest": ["library/oraclelinux:9"],
    "library/rockylinux:latest": ["library/rockylinux:9"],
    # these images have special tag layouts
    "library/notary:latest": ["library/notary:signer", "library/notary:server"],
    "library/opensuse:latest": ["opensuse/leap:latest", "opensuse/tumbleweed:latest"],
}

skip_map = {
    # these images have limited architecture builds available
    "library/clefos:latest": True,
    "library/docker-dev:latest": True,
    "library/ibm-semeru-runtimes:latest": True,
    "library/ubuntu-upstart:latest": True,
    "library/ubuntu-debootstrap:latest": True,
    "library/scratch:latest": True,
}

while True:
    response = requests.get(url)

    container_data = response.json()

    for i in container_data['results']:
        image = "{}/{}:latest".format(i['namespace'], i['name'])
        if image in skip_map:
            continue
        
        if image in convert_map:
            images = convert_map[image]
        else:
            images = [image]

        for i in images:
            istring = "docker.io/{}".format(i)
            output["containers"].append(istring)

    if container_data['next'] is None:
        for i in output["containers"]:
            print (i)
        sys.exit(0)

    url = container_data['next']
