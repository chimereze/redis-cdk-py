# redis_user_data.py

from aws_cdk import aws_ec2 as ec2
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Retrieve the Redis password
redis_password = config['redis']['password']

def master_user_data():
    user_data = ec2.UserData.for_linux()
    user_data.add_commands(
        "sudo apt update",
        "sudo apt install -y redis-server",
        "sudo sed -i 's/^# requirepass foobared/requirepass {redis_password}/' /etc/redis/redis.conf",
        "sudo systemctl restart redis.service"
    )
    return user_data

def slave_user_data():
    user_data = ec2.UserData.for_linux()
    user_data.add_commands(
        "sudo apt update",
        "sudo apt install -y redis-server",
        "echo 'replicaof redis-master 6379' | sudo tee -a /etc/redis/redis.conf",
        "echo 'masterauth {redispassword}' | sudo tee -a /etc/redis/redis.conf",
        "sudo systemctl restart redis.service"
    )
    return user_data

def client_user_data():
    user_data = ec2.UserData.for_linux()
    user_data.add_commands(
        "sudo apt update",
        "sudo apt install -y redis-tools"
    )
    return user_data
