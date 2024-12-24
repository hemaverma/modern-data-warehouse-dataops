import configparser
import os
import subprocess

# Get the current path of the Python file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the terraform directory
TF_DIR = os.path.join(CURRENT_DIR, "../e2e_samples/fabric_dataops_sample/infrastructure/terraform")

# Define the config file relative path
CONFIG_DIR = os.path.join(CURRENT_DIR, "../e2e_samples/fabric_dataops_sample/config")


def check_directory_exists(directory_path):
    print(f"checking {directory_path}")
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")


def get_terraform_output(variable_name):
    # Change directory to the specified path
    os.chdir(TF_DIR)

    # Run the terraform output command
    result = subprocess.run(["terraform", "output", "-raw", variable_name], capture_output=True, text=True)
    return result.stdout.strip()


def main():
    check_directory_exists(CURRENT_DIR)
    check_directory_exists(TF_DIR)

    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(f"{CONFIG_DIR}/application.cfg.template")

    # Replace placeholders with terraform output
    config["DEFAULT"]["workspace_name"] = get_terraform_output("workspace_name")
    config["DEFAULT"]["workspace_id"] = get_terraform_output("workspace_id")
    config["DEFAULT"]["lakehouse_name"] = get_terraform_output("lakehouse_name")
    config["DEFAULT"]["lakehouse_id"] = get_terraform_output("lakehouse_id")
    config["keyvault"]["name"] = get_terraform_output("keyvault_name")

    # Write the updated configuration back to a file
    with open(f"{CURRENT_DIR}/application.cfg", "w") as configfile:
        config.write(configfile)

    print("Configuration file updated successfully.")


if __name__ == "__main__":
    main()
