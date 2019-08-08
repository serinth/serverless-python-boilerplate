data "aws_security_groups" "vpc_security_groups" {
  filter {
    name   = "vpc-id"
    values = ["${module.vpc.vpc_id}"]
  }
}

output "vpc_security_group_ids" {
    value = "${data.aws_security_groups.vpc_security_groups}"
}

output "private_subnet_ids" {
    value = "${module.vpc.private_subnets}"
}