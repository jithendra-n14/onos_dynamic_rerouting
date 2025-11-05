#!/usr/bin/env python3
"""
onos_stats.py
-----------------
Fetches and prints device, link, and flow data from ONOS via its REST API.
Useful for verifying connectivity and REST API access.
"""

import requests
import json

ONOS_URL = "http://127.0.0.1:8181/onos/v1"
AUTH = ("onos", "rocks")  # Default ONOS credentials

def get_devices():
    """Return list of connected devices."""
    r = requests.get(f"{ONOS_URL}/devices", auth=AUTH)
    r.raise_for_status()
    return r.json().get("devices", [])

def get_links():
    """Return list of links."""
    r = requests.get(f"{ONOS_URL}/links", auth=AUTH)
    r.raise_for_status()
    return r.json().get("links", [])

def get_flows():
    """Return list of flows for all devices."""
    r = requests.get(f"{ONOS_URL}/flows", auth=AUTH)
    r.raise_for_status()
    flows = []
    data = r.json()
    for device in data.get("flows", []):
        device_id = device["deviceId"]
        for flow in device["flows"]:
            flows.append({
                "device": device_id,
                "id": flow["id"],
                "priority": flow["priority"],
                "state": flow["state"]
            })
    return flows

def main():
    print("\n=== Devices ===")
    for d in get_devices():
        print(f"- {d['id']} ({d['type']})")

    print("\n=== Flows ===")
    for f in get_flows():
        print(f"- {f['id']} on device {f['device']}")

    print("\n=== Links ===")
    for l in get_links():
        print(f"- {l['src']['device']} -> {l['dst']['device']}")

if __name__ == "__main__":
    main()
