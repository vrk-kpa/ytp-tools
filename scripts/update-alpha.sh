#! /bin/bash

set -e

source ~/ansible/hacking/env-setup

cd ~/code/ytp/
git pull
cd ~/code/ytp/ansible/vars/ytp-secrets
git pull
./secret.sh decrypt
cd ~/code/ytp/ansible
ansible-playbook --inventory-file=alpha-inventory -v cluster-dbserver.yml
ansible-playbook --inventory-file=alpha-inventory -v cluster-webserver.yml


