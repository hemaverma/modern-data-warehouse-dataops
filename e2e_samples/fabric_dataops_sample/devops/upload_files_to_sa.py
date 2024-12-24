import glob
import os

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from gen_application_config import get_terraform_output

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Retrieve storage account name and container name using get_terraform_output
STORAGE_ACCOUNT_NAME = get_terraform_output("storage_account_name")
CONTAINER_NAME = get_terraform_output("storage_container_name")
print(f"STORAGE_ACCOUNT_NAME: {STORAGE_ACCOUNT_NAME}, CONTAINER_NAME: {CONTAINER_NAME}")

if not STORAGE_ACCOUNT_NAME or not CONTAINER_NAME:
    raise ValueError("Please ensure that the storage account name and container name are correctly retrieved.")

# Initialize the BlobServiceClient with DefaultAzureCredential
credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net", credential=credential
)


def upload_file(file_path, blob_path):
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_path)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {file_path} to {blob_path}")


def main():
    # Define the file paths and their corresponding blob paths
    file_mappings = {
        f"{CURRENT_DIR}/application.cfg": "/config/application.cfg",
        f"{CURRENT_DIR}/../e2e_samples/fabric_dataops_sample/config/lakehouse_ddls.yaml": "/config/lakehouse_ddls.yaml",
    }

    # Add all CSV files in the seed directory to the file mappings
    csv_files = glob.glob(f"{CURRENT_DIR}/../e2e_samples/parking_sensors/data/seed/*.csv")
    for csv_file in csv_files:
        file_name = os.path.basename(csv_file)
        file_mappings[csv_file] = f"reference/{file_name}"

    # Upload each file to the corresponding blob path
    for file_path, blob_path in file_mappings.items():
        upload_file(file_path, blob_path)


if __name__ == "__main__":
    main()
