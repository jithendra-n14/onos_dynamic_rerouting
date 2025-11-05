#!/usr/bin/env python3
"""
dynamic_reroute.py
------------------
Monitors ONOS flows and links, reroutes traffic when a flow exceeds a threshold.
"""

import requests
import time

ONOS_URL = "http://127.0.0.1:8181/onos/v1"
AUTH = ("onos", "rocks")
PACKET_THRESHOLD = 500  # packet count threshold for rerouting

def get_devices():
    r = requests.get(f"{ONOS_URL}/devices", auth=AUTH)
    return r.json().get("devices", [])

def get_links():
    r = requests.get(f"{ONOS_URL}/links", auth=AUTH)
    return r.json().get("links", [])

def get_flows():
    r = requests.get(f"{ONOS_URL}/flows", auth=AUTH)
    flows = []
    data = r.json()
    for device in data.get("flows", []):
        for f in device.get("flows", []):
            flows.append({
                "id": f["id"],
                "device": device["deviceId"],
                "packets": f.get("packets", 0),
                "selector": f.get("selector"),
                "treatment": f.get("treatment")
            })
    return flows

def push_flow(device_id, flow_json):
    """Push a new flow rule to ONOS."""
    r = requests.post(f"{ONOS_URL}/flows/{device_id}", json=flow_json, auth=AUTH)
    if r.status_code in [200, 201]:
        print(f"[OK] Flow pushed to {device_id}")
    else:
        print(f"[ERR] Failed to push flow to {device_id}: {r.status_code} {r.text}")

def find_alternate_link(current_device, links):
    """Find an alternate active link for rerouting."""
    for link in links:
        if link["src"]["device"] != current_device and link["state"] == "ACTIVE":
            return link
    return None

def reroute_flows(flows, links):
    """Reroute congested flows."""
    for flow in flows:
        if flow["packets"] > PACKET_THRESHOLD:
            print(f"\n[!] Congested Flow {flow['id']} on {flow['device']} ({flow['packets']} packets)")
            alt = find_alternate_link(flow["device"], links)
            if not alt:
                print("  No alternate path found.")
                continue

            print(f"  Redirecting via {alt['src']['device']}:{alt['src']['port']} -> {alt['dst']['device']}:{alt['dst']['port']}")
            new_flow = {
                "priority": 40000,
                "timeout": 0,
                "isPermanent": True,
                "deviceId": flow["device"],
                "treatment": {
                    "instructions": [{"type": "OUTPUT", "port": alt["src"]["port"]}]
                },
                "selector": flow["selector"]
            }
            push_flow(flow["device"], new_flow)

def main():
    print("=== Starting ONOS Dynamic Rerouting ===\n")
    while True:
        links = get_links()
        flows = get_flows()

        print(f"\nChecked {len(flows)} flows across {len(links)} links.")
        reroute_flows(flows, links)
        time.sleep(10)

if __name__ == "__main__":
    main()
