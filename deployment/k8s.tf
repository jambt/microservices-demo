provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "docker-desktop"
}

module "server" {
  source = "./modules/simple-deployment"

  name         = "password-server"
  docker_image = docker_image.server
}

module "known-pw" {
  source = "./modules/simple-deployment"

  name         = "known-passwords"
  docker_image = docker_image.known-pw
}

module "dedup" {
  source = "./modules/simple-deployment"

  name         = "password-dedup"
  docker_image = docker_image.dedup
}

module "pw-checker" {
  source = "./modules/simple-deployment"

  name         = "password-checker"
  docker_image = docker_image.checker
}

module "redis" {
  source = "./modules/simple-deployment"

  name         = "redis"
  docker_image = docker_image.redis
  port = 6379
}

resource "kubernetes_service" "frontend" {
  metadata {
    name = "frontend"
  }
  spec {
    selector = {
      app = module.server.name
    }
    session_affinity = "ClientIP"
    port {
      port        = 8000
      target_port = 80
    }

    type = "LoadBalancer"
  }
}

