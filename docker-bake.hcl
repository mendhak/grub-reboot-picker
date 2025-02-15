variable "version" {
  default = ""
}

variable "suite" {
  default = ""
}

target "deb-builder" {
  dockerfile = "Dockerfile"
  tags = ["docker-deb-builder:latest"]
  args = {
    version = "${version}"
    suite = "${suite}"
  }
  output = ["type=docker"]
  
}