from kubernetes import client, config
import json
import boto3
import yaml
import os

def get_config():
    access_key_secret = os.environ.get("access_key", None)
    secret_access_key_secret = os.environ.get("secret_key", None)
    cluster_name = os.environ.get("secret_key", None)
    region_name = os.environ.get("region_name", None)
    s = boto3.Session(region_name=region_name)
    eks = s.client("eks",aws_access_key_id=access_key_secret, aws_secret_access_key=secret_access_key_secret)

    # get cluster details
    cluster = eks.describe_cluster(name=cluster_name)
    cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
    cluster_ep = cluster["cluster"]["endpoint"]
    cluster_name = cluster["cluster"]["arn"]
    cluster_short_name = cluster["cluster"]["name"]

    # build the cluster config hash
    cluster_config = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "cluster": {
                        "server": str(cluster_ep),
                        "certificate-authority-data": str(cluster_cert)
                    },
                    "name": str(cluster_name)
                }
            ],
            "contexts": [
                {
                    "context": {
                        "cluster": str(cluster_name),
                        "user": str(cluster_name)
                    },
                    "name": str(cluster_name)
                }
            ],
            "current-context": str(cluster_name),
            "preferences": {},
            "users": [
                {
                    "name": str(cluster_name),
                    "user": {
                        "exec": {
                            "apiVersion": "client.authentication.k8s.io/v1beta1",
                            "command": "aws",
                            "args": [
                                "--region", "us-east-1", "eks" , "get-token","--cluster-name",cluster_short_name,"--output","json"
                            ]
                        }
                    }
                }
            ]
        }

    # Write in YAML.
    config_text=yaml.dump(cluster_config, default_flow_style=False)
    open("my_kubeconfig.json", "w").write(config_text)

def getevc():
    get_config()
    try:
        # Load the Kubernetes configuration
        config.load_kube_config()
        
        # Read the kubeconfig from a file
        with open('my_kubeconfig.json') as f:
            kubeconfig = yaml.safe_load(f)
            config.load_kube_config_from_dict(kubeconfig)
        
        # Read the deployment specification from a YAML file
        with open(os.path.join(os.path.dirname(__file__), "nginx-deployment.yaml")) as f:
            dep = yaml.safe_load(f)
        
        # Create the Kubernetes AppsV1Api client
        k8s_apps_v1 = client.AppsV1Api()
        
        # Create the deployment in the default namespace
        resp = k8s_apps_v1.create_namespaced_deployment(
            body=dep, namespace="default"
        )
        print(f"Deployment created. status='{resp.metadata.name}'")
    
    except client.exceptions.ApiException as e:
        print(f"Exception when calling AppsV1Api->create_namespaced_deployment: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    getevc()