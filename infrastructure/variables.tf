variable "project" {
    description = "Project Name"
}
variable "cidr" {
    description = "VPC CIDR"
    default = "10.0.0.0/16"
}

variable "azs" {
    description = "availability zones"
    default = ["ap-southeast-2a", "ap-southeast-2c"]
}

variable "private_subnets" {
    default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnets" {
    default = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "enable_cognito" {
    description = "set to true if need to create a cognito user pool"
    default = false
}

variable "enable_nat_gateway" {
    description = "Default is 1 NAT per subnet. Check documentation for more options."
    default = true
}