#!/usr/bin/env python

# Script to configure AWS Regions and Hub Account in bulk for Prisma Cloud Agentless Scanning
# Usage: ./agentless-scanning-bulk-update.py

import os
import requests
from requests.packages import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

# Script variables that need to be updated
AWS_REGIONS = [] # List of AWS regions that will be scanned, example : AWS_REGIONS = ["eu-west-1","us-east-2"]
HUB_ACCOUNT = "" # Name or ID of the AWS account used as Hub to scan other accounts, refer to README.md for examples

# Set Credentials
console_url = os.getenv("COMPUTE_API_ENDPOINT")
access_key = os.getenv("PRISMA_USERNAME")
secret_key = os.getenv("PRISMA_PASSWORD")

payload = {
    'username':access_key,
    'password':secret_key
}

# Generate a Token for API authentication to Prisma Cloud
try:
    token = requests.post(console_url+"/api/v1/authenticate", json=payload, verify=0).json()['token']
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

# Set Prisma Cloud Headers for Login with token
pccHeaders = {
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/json'
}

# Init variables
limit = 50
offset = 0
success_counter = 0
overall_counter = 0
response = True

# Check that variables have been updated
if AWS_REGIONS != [] and HUB_ACCOUNT != "":
    while response:
        payload = {
            'limit':limit,
            'offset':offset,
            'cloudProviders':"aws"
        }

        # Query Prisma Cloud for existing accounts with agentless scanning enabled
        response = requests.get(console_url+"/api/v1/cloud-scan-rules", headers=pccHeaders, params=payload, verify=0).json()
        offset=offset+limit

        # Check API response and iterate through existing accounts
        if response:
            for i in response:
                # Ignore Hub account
                if i["agentlessScanSpec"]["hubAccount"] == False:
                    # Update configuration for the account : AWS Regions, Hub. 'Scanners' also needs to be 0 when scanning with a Hub account
                    i["agentlessScanSpec"]["regions"] = AWS_REGIONS
                    i["agentlessScanSpec"]["hubCredentialID"] = HUB_ACCOUNT
                    i["agentlessScanSpec"]["scanners"] = 0

                    # Initialize data and make the API call to update the account with its new configuration
                    data=[]
                    data.append(i)
                    update = requests.put(console_url+"/api/v1/cloud-scan-rules", headers=pccHeaders, json=data, verify=0)

                    # Check if API call was successful and update counters
                    if update.status_code == 200:
                        print(" + Successfully updated account :", i["credential"]["accountName"])
                        success_counter += 1
                        overall_counter += 1
                    else:
                        print(" - Something went wrong with account :", i["credential"]["accountName"])
                        overall_counter += 1

    # After iterating through all accounts, return the overall results
    if overall_counter != 0:
        if overall_counter == success_counter:
            print(f"   All accounts (total number : {success_counter}) have been successfully updated !")
        else:
            print(f"   {success_counter} accounts have been successfully updated\n   !!! {overall_counter - success_counter} accounts have NOT been updated !!!")
    else:
        print("   No accounts found on your Prisma Cloud tenant !")

else:
    print("!!! Please update values for AWS_REGIONS and HUB_ACCOUNT !!!")