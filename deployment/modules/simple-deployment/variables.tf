variable "name" {
  type        = string
  description = "Name of the simple deployment, used as name and label."
}

variable "docker_image" {
  description = "Docker image resource to deploy."
}

variable "replicas" {
  type        = number
  default     = 1
  description = "Number of replicas of this service (Default: 1)."
}

variable "port" {
  type        = number
  default     = 80
  description = "Port to be exposed."
}