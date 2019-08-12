# data "aws_security_groups" "vpc_security_groups" {
#   filter {
#     name   = "vpc-id"
#     values = ["${module.vpc.vpc_id}"]
#   }
# }

# output "vpc_security_group_ids" {
#   value = "${data.aws_security_groups.vpc_security_groups}"
# }

# output "private_subnet_ids" {
#   value = "${module.vpc.private_subnets}"
# }

data "aws_region" "current" {}

output "cognito_pool_arn" {
  value = "${element(concat(aws_cognito_user_pool.user_pool.*.arn, list("")), 0)}"
}

output "cognito_endpoint" {
  value = "${element(concat(aws_cognito_user_pool.user_pool.*.endpoint, list("")), 0)}"
}

output "user_pool_client_id" {
  value = "${element(concat(aws_cognito_user_pool_client.user_pool_client.*.id, list("")), 0)}"
}

output "user_pool_client_secret" {
  value = "${element(concat(aws_cognito_user_pool_client.user_pool_client.*.client_secret, list("")), 0)}"
  sensitive = true
}

output "cognito_domain" {
  value = "${var.enable_cognito_user_pool && !var.enable_cognito_custom_domain ? "https://${var.project}-${terraform.workspace}.auth.${data.aws_region.current.name}.amazoncognito.com" : ""}"
}