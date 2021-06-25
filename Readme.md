# Password Example

This is a very basic example to deploy microservices. It consists of 4
services:
* A frontend asking for a password and showing the results from the other
  services (`server`)
* A password-checker that calculates the password strengths (`password-checker`)
* A service that checks against a list of known passwords (`known-passwords`)
* A service that uses a redis backend to check if the given password is in
  the last 10 checked passwords (`password-dedup`).

## Installation
You need docker, terraform and a kubernetes cluster.

1. Adapt `deployment/k8s.tf` and change
   ```
   provider "kubernetes" {
     config_path    = "~/.kube/config"
     config_context = "docker-desktop"  # <-- ADAPT HERE
   }
   ```
   the value for `config_context` to your Kubernetes context.

2. Run `terraform apply` and confirm with `yes`. This will do the following:
   * Build the docker images
   * Deploy the services and deployments to K8s


## Uninstall
Run `terraform destroy` to remove all resources from K8s and the images.


## Easy testing:
The setup can be tested without K8s using `docker-compose up --build` from the main directory.
