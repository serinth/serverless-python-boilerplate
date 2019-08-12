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

variable "enable_nat_gateway" {
    description = "Default is 1 NAT per subnet. Check documentation for more options."
    default = true
}
variable "enable_cognito_user_pool" {
    description = "set to true if need to create a cognito user pool"
    default = true
}

variable "enable_cognito_custom_domain" {
    description ="set to true if managing the domain inside AWS otherwise use an ARN and custom generated ACM. By default an amazon domain will be used."
    default = false
}

variable "cognito_config" {
    type = "map"
    default = {
        email_verification_subject = "Device Verification Code"
        email_verification_message = "Verification Code {####}"
        default_email_option = "CONFIRM_WITH_CODE"
    }
}

variable "oauth_flows" {
    type = "map"
    default = {
        allowed_oauth_scopes = ["code", "implicit"]
        callback_urls = ["https://mydomain.com.au/callback/login"]
    }
}
