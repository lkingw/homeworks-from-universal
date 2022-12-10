# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.synced_folder ".", "/vagrant"
  config.vm.provider :virtualbox do |vb|
    vb.gui = true
  end
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install python3-pip -y
    pip3 install matplotlib
    pip3 install scapy==2.4.3
    pip3 install eventlet==0.30.2
    echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
    apt-get install mininet tshark -y
    git clone https://github.com/mininet/mininet
    mininet/util/install.sh -w
    pip3 install ryu pytest
  SHELL
end
