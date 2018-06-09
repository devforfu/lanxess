# -*- mode: ruby -*-
# vi: set ft=ruby :

$set_environment_vars = <<SCRIPT
tee "/etc/profile.d/vars.sh" > "/dev/null" <<EOF
export APP_DB_USER=lanxess
export APP_DB_PASS=reverse
export APP_DB_NAME=lanxess
export APP_SECRET=451249487b988c58a6cd7df51b89fbd0
export APP_CONFIG=default
EOF
SCRIPT

$set_extra_environment_vars = <<SCRIPT
tee "/etc/profile.d/extra_vars.sh" > "/dev/null" <<EOF
export APP_DB_URL_DEV=postgresql://${APP_DB_USER}:${APP_DB_PASS}@localhost:5432/${APP_DB_NAME}
export APP_DB_URL_TEST=postgresql://${APP_DB_USER}:${APP_DB_PASS}@localhost:5432/${APP_DB_NAME}
export APP_DB_URL_PROD=postgresql://${APP_DB_USER}:${APP_DB_PASS}@localhost:5432/${APP_DB_NAME}
EOF
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "parallels/ubuntu-16.04"

  config.vm.provider "parallels" do |prl|
    prl.name = "lanxess"
    prl.linked_clone = true
  end

  config.vm.provision "shell", inline: $set_environment_vars, run: "always"
  config.vm.provision "shell", inline: $set_extra_environment_vars, run: "always"

  config.vm.provision "shell", path: "provision/postgresql.sh"
  config.vm.provision "shell", path: "provision/python.sh"
  config.vm.provision "shell", path: "provision/env.sh"
  config.vm.synced_folder ".", "/vagrant"
  config.vm.synced_folder "src/", "/server"
  config.vm.network "forwarded_port", guest: 5432, host: 15432
  config.vm.network "forwarded_port", guest: 8080, host: 80
end
