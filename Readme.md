# Python Kubernetes EKS Deployment Script

This Python script automates the process of configuring a Kubernetes cluster and deploying an application to it on Amazon EKS. It fetches the necessary configuration details from AWS and uses the Kubernetes Python client to create the deployment.

## Prerequisites

**Python 3.x**: Installed with `boto3`, `kubernetes`, `pyyaml`, and `json` libraries.

## Environment Variables

Set the following environment variables before running the script:

- `access_key`: Your AWS access key ID.
- `secret_key`: Your AWS secret access key.
- `cluster_name`: The name of your EKS cluster.
- `region_name`: The AWS region where your EKS cluster is located.

## Files

- `nginx-deployment.yaml`: The YAML file containing the deployment specification for your application. Place this file in the same directory as the script.

## Usage

1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required Python packages**:
   ```sh
   pip install boto3 kubernetes pyyaml
   ```

3. **Set the environment variables**:
   ```sh
   export access_key=<your-aws-access-key>
   export secret_key=<your-aws-secret-key>
   export cluster_name=<your-cluster-name>
   export region_name=<your-region-name>
   ```

4. **Run the script**:
   ```sh
   python script.py
   ```
