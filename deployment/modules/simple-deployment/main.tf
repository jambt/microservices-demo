resource "kubernetes_deployment" "this" {
  metadata {
    name = var.name
    labels = {
      app = var.name
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.name
      }
    }

    template {
      metadata {
        labels = {
          app = var.name
        }
      }

      spec {
        container {
          image             = var.docker_image.name
          name              = var.name
          image_pull_policy = "IfNotPresent"
        }
      }
    }
  }
}

resource "kubernetes_service" "this" {
  metadata {
    name = var.name
  }
  spec {
    selector = {
      app = kubernetes_deployment.this.metadata.0.labels.app
    }
    port {
      port = var.port
    }
  }
}
