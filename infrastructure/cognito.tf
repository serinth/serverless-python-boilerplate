resource "aws_cognito_user_pool" "user_pool" {
    name = "${var.project}-${terraform.workspace}-user-pool"
    count = "${var.enable_cognito_user_pool ? 1 : 0}"
    
    alias_attributes = ["email", "preferred_username"]
    auto_verified_attributes = ["email"]
    email_verification_subject = "${var.project} - ${var.cognito_config["email_verification_subject"]}"
    email_verification_message = "${var.cognito_config["email_verification_message"]}"
    

    verification_message_template {
        default_email_option = "${var.cognito_config["default_email_option"]}"
    }

    password_policy {
        minimum_length    = 10
        require_lowercase = true
        require_numbers   = true
        require_symbols   = true
        require_uppercase = true
    }

    schema {
        attribute_data_type      = "String"
        developer_only_attribute = false
        mutable                  = false
        name                     = "email"
        required                 = true

        string_attribute_constraints {
            min_length = 7
            max_length = 15
        }
    }

    tags = {
        Terraform = "true"
        Environment = "${terraform.workspace}"
        Project = "${var.project}"
    }

}


resource "aws_cognito_user_pool_client" "user_pool_client" {
    name = "${var.project}-${terraform.workspace}-user-pool-client"
    count = "${var.enable_cognito_user_pool ? 1 : 0}"
    user_pool_id = "${join("", aws_cognito_user_pool.user_pool.*.id)}"

    generate_secret     = true
    explicit_auth_flows = ["ADMIN_NO_SRP_AUTH"]

    allowed_oauth_flows = "${var.oauth_flows["flows"]}"
    allowed_oauth_flows_user_pool_client = true
    callback_urls = "${var.oauth_flows["callback_urls"]}"
    supported_identity_providers = ["COGNITO"]

    allowed_oauth_scopes = ["openid", "email"]
}

resource "aws_cognito_user_pool_domain" "aws_domain" {
  domain = "${var.project}-${terraform.workspace}"
  count = "${var.enable_cognito_user_pool && !var.enable_cognito_custom_domain ? 1 : 0}" 
  user_pool_id = "${join("", aws_cognito_user_pool.user_pool.*.id)}"
}


# Custom Domain, Assumes the domain is already purchased in Route53 and has an A record
data "aws_route53_zone" "domain_zone"{
    name = "${var.domain}"
}

resource "aws_acm_certificate" "cert" {
    domain_name = "${terraform.workspace}.auth.${var.domain}"
    validation_method= "DNS"
    provider = "aws.east1"

    subject_alternative_names = [
        "*.${terraform.workspace}.auth.${var.domain}",
        "*.auth.${var.domain}",
        "*.${var.domain}"
    ]
}

locals {
    dvo = "${flatten(aws_acm_certificate.cert.*.domain_validation_options)}"
}

resource "aws_route53_record" "cert_validation" {
    count = 3 #the subject alt names count
    zone_id = "${data.aws_route53_zone.domain_zone.zone_id}"
    ttl = 60
    name = "${lookup(local.dvo[count.index], "resource_record_name")}"
    type = "${lookup(local.dvo[count.index], "resource_record_type")}"
    records = ["${lookup(local.dvo[count.index], "resource_record_value")}"]
    allow_overwrite = true
}

# Open Issue if it throws can't find DNS record error:
# https://github.com/terraform-providers/terraform-provider-aws/issues/8597
# resource "aws_acm_certificate_validation" "cert" {
#     provider = "aws.east1"
#     count = 3
#     certificate_arn = "${element(aws_acm_certificate.cert.*.arn, count.index)}"
#     validation_record_fqdns = "${aws_route53_record.cert_validation.*.fqdn}"
# }


# resource "aws_cognito_user_pool_domain" "custom_domain" {
#   domain = "${terraform.workspace}.auth.${var.domain}"
#   count = "${var.enable_cognito_user_pool && var.enable_cognito_custom_domain ? 1 : 0}" 
#   user_pool_id = "${join("", aws_cognito_user_pool.user_pool.*.id)}"
#   certificate_arn = "${join("", aws_acm_certificate_validation.cert.*.certificate_arn)}"
# }

# This is the workaround until the above issue gets resolved.
resource "aws_cognito_user_pool_domain" "custom_domain" {
  domain = "${terraform.workspace}.auth.${var.domain}"
  count = "${var.enable_cognito_user_pool && var.enable_cognito_custom_domain ? 1 : 0}" 
  user_pool_id = "${join("", aws_cognito_user_pool.user_pool.*.id)}"
  certificate_arn = "${join("", aws_acm_certificate.cert.*.arn)}"
}
