import requests
import os
from dotenv import load_dotenv

load_dotenv()

org_name = os.getenv("ORG_NAME")
registry_name = "private"
provider_name = os.getenv("PROVIDER_NAME")
token = os.getenv("TERRAFORM_CLOUD_TOKEN")
base_url = "https://app.terraform.io/api/v2"

def create_provider_if_doesnt_exist():
    if does_provider_exist():
        print("Provider found")
        return
    create_provider()

def get_auth_headers():
    return {
        'content-type': 'application/vnd.api+json',
        'Authorization': f'Bearer {token}'
    }

def does_provider_exist():
    url = f"{base_url}/organizations/{org_name}/registry-providers/{registry_name}/{org_name}/{provider_name}"
    headers = get_auth_headers()
    response = requests.get(url, headers = headers)
    return response.ok

def create_provider():
    url = f"{base_url}/organizations/{org_name}/registry-providers"
    body = {
          "data": {
            "type": "registry-providers",
            "attributes": {
                "name": provider_name,
                "namespace": org_name,
                "registry-name": "private"
            }
        }
    }
    response = requests.post(url, json = body, headers = get_auth_headers())
    print(f"Provider creation returned response: {response.text}")


def run():
    create_provider_if_doesnt_exist()
