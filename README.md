# Scripts for automating server provision

IMPORTANT: WE CANT COMPLETELY RELY ON PURE ANSIBLE DUE TO LACK OF PROPER SUPPORT FOR IT IN GCP ANSIBLE PLUGIN - E.G. NO CLOUD NAT/CLOUD RUN. SEEING THIS, WE HAVE TO RESORT TO USING SOMETHING LIKE TERRAFORM TO PROVISION AND MAYBE USE ANSIBLE ONLY FOR CONFIGURATION WORK.

Contains some of the common commands to be able to provisions servers rather than ssh-ing in and run the commands over and over again across multiple servers. Here is a list of some of the possible things that can be setup from the following ansible scripts:

A few additional notes:

- For some of the components, especially databases, it might good to also add cron jobs and scripts to do automated backups of the data to relevant data stores

# Components

## Language Runtimes

- [x] r
- [x] python3
- [x] java

## Databases

- [ ] mysql
- [ ] postgresql
- [ ] cassandra
- [ ] couchdb
- [ ] redis
- [ ] redis cluster
- [x] elasticsearch
- [ ] cockroachdb

## Application Services

- [x] rstudio server
- [ ] r shiny server
- [ ] airflow
- [ ] jenkins
- [ ] ansible (on server)
- [ ] nginx server setup (with python app)

## Logging/Monitoring Services (Part of logging stack)

- [ ] logstash
- [ ] filebeats
- [ ] fluentd
- [ ] prometheus

## Messaging Services

- [ ] kafka
- [x] nats

## Microservice tooling

- [x] docker
- [x] docker with docker-compose
- [x] docker swarm
- [ ] kubernetes
- [ ] etcd
- [x] consul
- [ ] zookeeper

# Setting this up locally

Setting up python virtual environment for this

```bash
virtualenv env
source ./env/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install ansible
```

For debugging

```bash
# Prints debugging value: test as well as current os version
ansible-playbook sample.yml --tags debug -e "name=test" -i hosts
```

Installing the various cloud providers (Currently using other cli tools in order to help combine these scripts together. Less code and configuration to handle and manage)

- [gcloud](https://cloud.google.com/sdk/docs/quickstart-macos)

Setting up a full blown set of useful services?

ansible.json is a service account file from a GCP project

```bash
GOOGLE_APPLICATION_CREDENTIALS=ansible.json ansible-playbook playbook-dc-create.yml -e '{"gcp_project": "XXXX", "gcp_cred_kind": "application","ansible_user":"XXX","ansible_ssh_private_key_file":"~/.ssh/google_compute_engine"}'
```

# Examples

## Setting up docker on a debian machine on Google VM

It is possible to just go for a container optimized google VM but let's just complete this exercise to see how to get it up and running. This is to allow us to also kind of apply the same ansible scripts to other machines/vms in even if they don't have the images that already container it.

```bash
# Create instance
# It might be necessary to add --project and other flags if you're working across projects
gcloud beta compute instances create instance-3 --zone=us-central1-c --machine-type=e2-medium --subnet=default --tags=http-server,https-server --image=projects/debian-cloud/global/images/debian-10-buster-v20220406 --image-project=debian-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=instance-3

# Another option is to create a ubuntu instance instead
gcloud beta compute instances create instance-1 --zone=us-central1-c --machine-type=n1-standard-1 --subnet=default --tags=http-server,https-server --image=ubuntu-1604-xenial-v20180912 --image-project=ubuntu-os-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=instance-1

# SSH into instance
# Sets up ssh keys for you both locally and on the remote-machine
gcloud compute ssh instance-1

# Check to ensure that instances are create
gcloud compute instances list

# Check that you can ssh in
ssh {name}@{ip address of instance-1}
```

Add the ip address to the hosts file under docker. Then, run the following command.

```bash
ansible-playbook infra.yml --tags docker -e "user={ add the name being used to ssh into instance-1 here }" -i hosts
```

We can extend it further by also installing docker-compose as well

```bash
ansible-playbook infra.yml -e "user={ add the name being used to ssh into instance-1 here }" -e "docker_user={ your dockerhub username }" -e "docker_pw={ your password on dockerhub for the account specified }" -i hosts
```

We can then `ssh` into the service and run our various docker commands

For cleaning up:

```
gcloud compute instances delete instance-1
```

Notes: In the case where hosts use password to authenticate instead of ssh keys.

- Install the following: sshpass
- Use host `{host ip} ansible_connection=ssh ansible_ssh_user={user} ansible_ssh_pass={pw}`
- If sudo need password... add an extra param to the cmd: `ansible_sudo_pass={pw}` to use password for authentication

## Notes

FYI... For roles such as the `hadoop` role, it requires to downgrade to non sudo user before running certain commnads. Unfortunately, normal ansible playbook commands won't work as expected here; need to use ANSIBLE_SSH_PIPELINING. Reason for this is as ansible requires all commands to be secure, so any command with non-sudo user would require to set the file permissions to 777 -> which is world-readable which is bad for security. Exact reason why Ansible ssh pipelining is available on ansible website.

```bash
ANSIBLE_SSH_PIPELINING=1 ansible-playbook  -i hosts infra.yml   
```