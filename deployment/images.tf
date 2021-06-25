terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.13.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "server" {
  name = "pw-server"
  build {
    path = "../server"
    tag  = ["pw-server:v1"]
  }
}

resource "docker_image" "known-pw" {
  name = "pw-known"
  build {
    path = "../known-passwords"
    tag  = ["pw-known:v1"]
  }
}

resource "docker_image" "dedup" {
  name = "pw-dedup"
  build {
    path = "../password-dedup"
    tag  = ["pw-dedup:v1"]
  }
}

resource "docker_image" "checker" {
  name = "pw-checker"
  build {
    path = "../password-checker"
    tag  = ["pw-checker:v1"]
  }
}

resource "docker_image" "redis" {
  name = "redis"
}
