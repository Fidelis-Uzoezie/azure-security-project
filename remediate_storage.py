import os
import sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

def main():
    try:
        credential = DefaultAzureCredential()
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

        if not subscription_id:
            print("[-] Error: AZURE_SUBSCRIPTION_ID environment variable is missing.")
            sys.exit(1)

        storage_client = StorageManagementClient(credential, subscription_id)
        print(f"[+] Authenticated successfully. Scanning subscription: {subscription_id}\n")
    except Exception as e:
       print(f"[-] Authentication failed: {e}")
       sys.exit(1)

    try:
        storage_accounts = storage_client.storage_accounts.list()
    except Exception as e:
        print(f"[-] Failed to retrieve storage accounts: {e}")
        sys.exit(1)

    for account in storage_accounts:
        parts = account.id.split("/")
        resource_group = parts[parts.index("resourceGroups") + 1] if "resourceGroups" in parts else "unknown"
        account_name = account.name

        print(f"[*] Checking storage account: {account_name} [RG: {resource_group}]")

        if account.allow_blob_public_access is True or account.allow_blob_public_access is None:
            print(f"  [!] RISK IDENTIFIED: Public blob access is enabled or unconfigured.")
            print(f"  [+] Executing self-healing remediation: Disabling public access...")

            try:
                storage_client.storage_accounts.update(
                    resource_group_name=resource_group,
                    account_name=account_name,
                    parameters={"allow_blob_public_access": False}
                )
                print(f"  [✓] SUCCESS: Public access disabled for {account_name}.\n")
            except Exception as e:
                print(f"  [-] REMEDIATION FAILED for {account_name}: {e}\n")
        else:
            print(f"  [✓] Compliant: Public blob access is explicitly disabled.\n")

if __name__ == "__main__":
    main()
