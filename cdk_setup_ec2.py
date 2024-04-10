"""
This module defines a AWS CDK stack that sets up a Redis cluster using EC2 instances in AWS.
Creates a VPC, an Ubuntu-based EC2 instance for the Redis master, slave instances for replication,
and a client instance with Redis tools installed. Security groups are configured to allow SSH access
and Redis default port access.
"""


from aws_cdk import core, aws_ec2 as ec2

# Import the user data functions
from redis_userdata import master_user_data, slave_user_data, client_user_data


class RedisCdkSetupPythonStack(core.Stack):
    """Define a stack to set up a Redis cluster on AWS using CDK."""

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        """Initialize the Redis setup stack.

        Args:
            scope (core.Construct): Scope in which this stack is defined.
            id (str): Identifier for this stack.
        """
        super().__init__(scope, id, **kwargs)

        # Create a new VPC
        vpc = ec2.Vpc(self, "VPC")

        # Define an Ubuntu AMI
        ubuntu_ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        # Security Group allowing SSH and Redis default port
        security_group = ec2.SecurityGroup(
            self, "RedisSecurityGroup",
            vpc=vpc,
            description="Allow SSH and Redis access",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH Access"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(6379), "Redis Port"
        )

        # EC2 Instance configurations
        instance_type = ec2.InstanceType("t3.micro")

        # Create instances with user data
        ec2.Instance(self, "RedisMaster",
                     instance_type=instance_type,
                     machine_image=ubuntu_ami,
                     vpc=vpc,
                     security_group=security_group,
                     user_data=master_user_data())

        ec2.Instance(self, "RedisSlave",
                     instance_type=instance_type,
                     machine_image=ubuntu_ami,
                     vpc=vpc,
                     security_group=security_group,
                     user_data=slave_user_data())

        ec2.Instance(self, "RedisClient",
                     instance_type=instance_type,
                     machine_image=ubuntu_ami,
                     vpc=vpc,
                     security_group=security_group,
                     user_data=client_user_data())
