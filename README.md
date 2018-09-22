# Scripts for automating server provision

Contains some of the common commands to be able to provisions servers rather than ssh-ing in and run the commands over and over again across multiple servers. In some of the cases, we would want to run

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
gcloud beta compute instances create instance-1 --zone=us-central1-c --machine-type=n1-standard-1 --subnet=default --tags=http-server,https-server --image=debian-9-stretch-v20180911 --image-project=debian-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=instance-1

# SSH into instance
# Sets up ssh keys for you both locally and on the remote-machine
gcloud compute ssh instance-1

# Check to ensure that instances are create
gcloud compute instances list

# Check that you can ssh in
ssh {name}@{ip address of instance-1}
```

Add the ip address to the hosts file under docker. Then, run the following command

```bash
ansible-playbook infra.yml --tags installDocker -e "user={ add the name being used to ssh into instance-1 here }" -i hosts
```

We can then `ssh` into the service and run our various docker commands

For cleaaning up:

```
gcloud compute instances delete instance-1
```
