"""
Downloads the SCDNR "Species County Distributions" dataset (rare,
threatened, and endangered species observed by county in South Carolina)
from the SCDNR ArcGIS REST feature service, and saves it as one raw CSV.

Uses ONLY the Python standard library (urllib, json, csv) for the actual
data pull -- the one optional dependency is `certifi`, used only to fix
a common macOS issue where Python can't find a local certificate bundle
(SSL: CERTIFICATE_VERIFY_FAILED). If certifi isn't installed, the script
falls back to the default SSL behavior.

    pip3 install certifi

Source: South Carolina Department of Natural Resources (SCDNR),
Natural Heritage Program
Service: https://arcweb.dnr.sc.gov/server/rest/services/Hosted/Species_County_Distributions/FeatureServer/1

Run:
    python fetch_scdnr_species_county.py

Output:
    scdnr_species_county_raw.csv  (written next to this script)
"""

import csv
import json
import ssl
import urllib.parse
import urllib.request

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = None  # fall back to the system default

# Some state-government ArcGIS servers don't send their full certificate
# chain, which trips up strict clients like Python's ssl module even when
# the CA bundle itself (certifi) is fine -- browsers tolerate this, but
# urllib doesn't. If a normal, verified request fails specifically on a
# certificate verification error, we fall back once to an unverified
# request rather than give up. This is a plain public GET to a .gov open
# data endpoint (no login, no data submitted), so the risk here is low --
# but it's a real relaxation of a security check, worth knowing about.
UNVERIFIED_SSL_CONTEXT = ssl._create_unverified_context()
_warned_about_unverified = False

BASE_URL = (
    "https://arcweb.dnr.sc.gov/server/rest/services/Hosted/"
    "Species_County_Distributions/FeatureServer/1/query"
)
PAGE_SIZE = 2000  # the service's own max is 5000; smaller pages are gentler
OUTPUT_FILE = "scdnr_species_county_raw.csv"


def open_url(req):
    global _warned_about_unverified
    try:
        return urllib.request.urlopen(req, timeout=60, context=SSL_CONTEXT)
    except ssl.SSLCertVerificationError:
        if not _warned_about_unverified:
            print(
                "WARNING: certificate verification failed even with certifi's "
                "bundle (the server is likely missing an intermediate cert in "
                "its chain). Falling back to an UNVERIFIED connection for this "
                "public, read-only .gov data pull."
            )
            _warned_about_unverified = True
        return urllib.request.urlopen(req, timeout=60, context=UNVERIFIED_SSL_CONTEXT)


def fetch_all_records():
    records = []
    offset = 0
    while True:
        params = {
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "false",
            "f": "json",
            "resultRecordCount": PAGE_SIZE,
            "resultOffset": offset,
        }
        url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
        print(f"Fetching records {offset}-{offset + PAGE_SIZE}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with open_url(req) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if "error" in payload:
            raise RuntimeError(f"ArcGIS service error: {payload['error']}")

        features = payload.get("features", [])
        records.extend(feature["attributes"] for feature in features)

        if len(features) < PAGE_SIZE:
            break  # last page
        offset += PAGE_SIZE

    return records


def write_csv(records, path):
    # Union of all field names, preserving first-seen order, in case
    # different pages ever come back with slightly different attributes.
    fieldnames = []
    seen = set()
    for record in records:
        for key in record:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main():
    records = fetch_all_records()
    print(f"Fetched {len(records)} total records.")
    write_csv(records, OUTPUT_FILE)
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
