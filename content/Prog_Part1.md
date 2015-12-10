Title: Part 1 - How to set up a development environment for data analysis in python
Date: 2015-12-10 12:00
Category: Python
Tags: Vagrant, Docker, Python
Slug: development-environment
Authors: Frederic Husser
Summary: Set-up of a virtual development environment

In this first tutorial, we are making sure that all the tools are set up for doing some data analysis in Python. Some developers might be working on Linux, Mac or sometimes on Windows. Programming with Python on Windows is a real pain, but a debate on the OS is out of the scope of this blog.

Instead, we will focus on making the environment totally agnostic on your choice and habits. We will use Vagrant for creating and configuring a linux Ubuntu virtual machine. From the Vagrant configuration file (the vagrantfile), we make sure that the virtual machine is provisioned with all dependencies we will need for developing our machine learning and web applications.

Before starting make sure that you do have this three softwares installed on your machine:
-   VirtualBox
-   Vagrant
-   Git

Configuring a Linux Ubuntu machine
----------------------------------
Create a directory in which you will start the project. Of course the repository with all the code is available on GitHub, so that you can get started faster by cloning it.

In order to stress on the most important parts of our setup, we will go through the configuration ste-by-step.

'''bash
$ mkdir collective-intelligence
$ cd collective-intelligence
'''

We will create a Vagrant configuration file Vagrantfile that will contain all information necessary to build and run the virtual machine.

'''
VAGRANTFILE\_API\_VERSION = "2"
Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.hostname = "vagrant-docker-anaconda"
    config.vm.network "private\_network", ip: "192.168.50.100"
    config.vm.network "forwarded\_port", guest: 80, host: 8080
    config.vm.provider :virtualbox do |vb|
        vb.customize \["modifyvm", :id, "--memory", "1024", "--cpus", "2"\]
    end
    config.vm.provision :docker
    config.vm.provision :docker\_compose, yml: "/vagrant/docker-compose.yml", rebuild: true, run: "always"
    end
'''

Provisioning with the necessary software

We will be using a Linux Ubuntu machine with the following software installed:

-   A python distribut
