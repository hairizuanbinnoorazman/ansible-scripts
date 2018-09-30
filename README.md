# Scripts for automating server provision

Contains some of the common commands to be able to provisions servers rather than ssh-ing in and run the commands over and over again across multiple servers. Here is a list of some of the possible things that can be setup from the following ansible scripts:

- [ ] ansible (on server)
- [x] docker
- [x] docker with docker-compose
- [x] docker swarm
- [x] r
- [x] rstudio server
- [ ] airflow
- [ ] r shiny server
- [ ] jenkins
- [ ] kubernetes
- [ ] nginx server setup (with python app)
- [ ] elasticsearch
- [ ] logstash
- [ ] filebeats
- [ ] fluentd
- [ ] prometheus
- [ ] mysql
- [ ] postgresql
- [ ] cassandra
- [ ] couchdb
- [ ] redis
- [ ] redis cluster

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

# Examples

## Setting up docker on a debian machine on Google VM

It is possible to just go for a container optimized google VM but let's just complete this exercise to see how to get it up and running. This is to allow us to also kind of apply the same ansible scripts to other machines/vms in even if they don't have the images that already container it.

```bash
# Create instance
# It might be necessary to add --project and other flags if you're working across projects
gcloud beta compute instances create instance-2 --zone=us-central1-c --machine-type=n1-standard-1 --subnet=default --tags=http-server,https-server --image=debian-9-stretch-v20180911 --image-project=debian-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=instance-2

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
