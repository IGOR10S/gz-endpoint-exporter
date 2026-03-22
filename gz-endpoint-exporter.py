#!/usr/bin/env python3

import requests
import base64
import uuid
import csv

API_KEY = "YOUR_API_KEY"
GZ_URL = "https://cloudgz.gravityzone.bitdefender.com/api/v1.0/jsonrpc/network"

EXPORT_FILE = "endpoints.csv"
PER_PAGE = 100
TIMEOUT = 30

# Basic Auth: api_key:
auth_str = f"{API_KEY}:"
auth_b64 = base64.b64encode(auth_str.encode()).decode()

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_b64}"
}


def get_all_endpoints():
    page = 1
    all_items = []
    total = None

    with requests.Session() as session:
        session.headers.update(HEADERS)

        while True:
            payload = {
                "jsonrpc": "2.0",
                "method": "getNetworkInventoryItems",
                "params": {
                    "page": page,
                    "perPage": PER_PAGE,
                    "filters": {
                        "depth": {
                            "allItemsRecursively": True
                        }
                    }
                },
                "id": str(uuid.uuid4())
            }

            response = session.post(GZ_URL, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            error = data.get("error")
            if error:
                raise RuntimeError(error)

            result = data.get("result", {})
            items = result.get("items", [])

            if total is None:
                total = result.get("total", 0)

            all_items.extend(items)

            # Correct stop condition
            if not items or page * PER_PAGE >= total:
                break

            page += 1

    return all_items


def format_ep(ep, details):
    return f"{ep.get('name')} - {details.get('ip')} - {details.get('operatingSystemVersion')}"


def export_csv(endpoints, filename=EXPORT_FILE):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(["Endpoint Name", "IP", "OS", "Managed Status"])

        for ep in endpoints:
            details = ep.get("details") or {}
            name = ep.get("name", "")
            ip = details.get("ip", "")
            os = details.get("operatingSystemVersion", "")
            is_managed = details.get("isManaged")
            
            if is_managed is True:
                status = "Managed"
            elif is_managed is False:
                status = "Unmanaged"
            else:
                status, ip, os = "None", "None", "None"

            writer.writerow([name, ip, os, status])


def main():
    print("Endpoints retrieval from GravityZone...")

    endpoints = get_all_endpoints()
    managed = []
    unmanaged = []
    unknown = []

    for ep in endpoints:
        details = ep.get("details") or {}
        is_managed = details.get("isManaged")

        if is_managed is True:
            managed.append((ep, details))
        elif is_managed is False:
            unmanaged.append((ep, details))
        else:
            unknown.append((ep, details))
    
    print(f"\n====================[*] Total entities found: {len(endpoints)}")

    print(f"\n====================[+] Managed endpoints: {len(managed)}")
    # for ep, details in managed:
    #     print(format_ep(ep, details))

    print(f"\n====================[-] Unmanaged endpoints: {len(unmanaged)}")
    # for ep, details in unmanaged:
    #     print(format_ep(ep, details))
    
    print(f"\n====================[?] Unknown Endpoints: {len(unknown)}")
    # for ep, details in unknown:
    #     print(format_ep(ep, details))

    export_csv(endpoints)
    print(f"\nExport completed: {EXPORT_FILE}")


if __name__ == "__main__":
    main()
