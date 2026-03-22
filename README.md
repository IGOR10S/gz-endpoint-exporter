# GravityZone Endpoints Inventory Exporter

This Python script allows you to query the **Bitdefender GravityZone** platform to get the complete inventory of endpoints present in the network.

## Requirements

- Python 3.7+
- Python modules:
  - `requests`
  - `base64` (standard library)
  - `uuid` (standard library)
  - `csv` (standard library)
- Valid API Key for Bitdefender GravityZone
- API Access: `https://cloudgz.gravityzone.bitdefender.com/api/v1.0/jsonrpc/network`

Dependency Installation:

```bash
pip install requests
```

## Features

- Full endpoint recovery from GravityZone via **JSON-RPC** API
- Automatic pagination management
- Endpoint classification:
  - Managed
  - Unmanaged
  - Unknown
- Export data to CSV format
- API Error Handling
- Console-readable output with summary statistics
- Configurable timeout support

## Description

Using the `getNetworkInventoryItems` API, the script:

- Make paginated requests to retrieve all available endpoints
- Aggregate results until completion
- Analyze each endpoint to determine its management status (`isManaged`)
- Extract key information:
  - Endpoint name
  - IP address
  - Operating System
  - Status (`Managed` / `Unmanaged` / `None`)
- The data is finally exported to a CSV file (`endpoints.csv`), ready for analysis or integration into other systems

> [!NOTE]
> Authentication is handled via **Basic Auth**, using a **Base64-encoded Key API**.

## Example

Enter your own API Key:

```python
API_KEY = "YOUR_API_KEY"
```

Run the script

```bash
python gz-endpoint-exporter.py
```

Console output

```text
Endpoints retrieval from GravityZone...

====================[*] Total entities found: 250

====================[+] Managed endpoints: 180

====================[-] Unmanaged endpoints: 60

====================[?] Unknown Endpoints: 10

Export completed: endpoints.csv
```

Generated report (`endpoints.csv`)

| Endpoint Name        | IP           | OS           | Managed Status |
| -------------------- | ------------ | ------------ | -------------- |
| PC-01                | 192.168.1.10 | Windows 10   | Managed        |
| PC-02                | 10.50.0.11   | Ubuntu 22.04 | Unmanaged      |
| Computers and Groups | None         | None         | Unknown        |
| ...                  | ...          | ...          | ...            |
