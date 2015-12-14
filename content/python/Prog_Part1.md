Title: Part 1 - Python Data Analysis environment with Vagrant, Docker and Anaconda
Date: 2015-12-10 12:00
Category: Python
Tags: Vagrant, Docker, Python, Anaconda
Slug: development-environment
Authors: Frederic Husser
Summary: We will fire up a virtual development environment using state-of-art tools for making data analysis in Python. We will use both Vagrant and Docker for firing up a Linux virtual machine with all tools ready for Python data analysis. Preparing the Python environment is sometimes hard for scientists without a strong background in software development, this is wy having a reproducible and turnkey workflow is so important. Additionally when it comes to collaboration, the installation of the Python interpreters as well as all the needed packages can become a real pain. With virtual environment, you are making sure that everybody is working under the same settings.

In this tutorial, we build an environment with Vagrant, Docker and Anaconda for doing firstly data analysis in Python. It should be totally agnostic on the choice of your operating system, be it Linux, Mac or Windows. Vagrant is used for configuring the linux Ubuntu virtual machine. The vagrant file located at the root of the project directory contains all the settings for that VM so that it can boot with all dependencies provisioned 

Before starting make sure that you do have this three softwares installed on your machine:

- VirtualBox
- Vagrant
- Git

Configuring a Linux Ubuntu machine
----------------------------------
Create a directory in which you will start the project. Of course the repository with all the code is available on GitHub, so that you can get started faster by cloning it.

In order to stress on the most important parts of our setup, we will go through the configuration ste-by-step.

```bash
$ mkdir collective-intelligence
$ cd collective-intelligence
```

We will create a Vagrant configuration file Vagrantfile that will contain all information necessary to build and run the virtual machine. We setup the name of the VM, the network settings and port forwarding. We also add a synchronized folder so that all changes in the file system of the host machine are taken into account in the file system of the guest. 

```
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.hostname = "vagrant-docker-anaconda"
    config.vm.network "private_network", ip: "192.168.50.100"
    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024", "--cpus", "2"]
    end
    
    config.vm.synced_folder ".", "/vagrant", :type => "nfs"
    end
```

Once the Vagrantfile is defined you are able to build and run the VM simply by typing:

```bash
$ vagrant up
```

Provisioning with the necessary software
----------------------------------------

For starting developping applications for data analysis we need a Python distribution. For data analysis in Python, Anaconda offered by Continuum Analytics is very convenient, and contains all the necessary packages. First connect through ssh to your running VM in one command line.

```bash
$ vagrant ssh
```

Then we will install anaconda. From the bash terminal connected to your VM, you can install Anaconda

```bash
$ sudo apt-get update

# Download from the Anaconda remote directory
$ sudo wget http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/Anaconda-2.1.0-Linux-x86_64.sh

# Install the Anaconda distribution in batch mode
$ sudo bash Anaconda-2.1.0-Linux-x86_64.sh -b

# Append the path of the Anaconda Python interpreter into your path
$ export PATH="/home/vagrant/anaconda/bin:$PATH"

# Update the package manager and install pymongo as we will use it
$ sudo conda update -y conda
$ sudo conda install -y pymongo
```

Now you are all set and ready to work with Python. You can check your installation by starting the Python interpreter.

```bash
vagrant@vagrant-docker-anaconda:~$ python
Python 2.7.10 |Anaconda 2.1.0 (64-bit)| (default, Oct 19 2015, 18:04:42)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
>>>
```

Using Docker for our database and web application
-------------------------------------------------

Now we are almost ready to develop our machine learning application ! We also want to have a MongoDB and Postgres SQL instances running, as well as a web application (in Python of course!). We will use Docker and Docker-Compose for that and build a multi-container application. Basically we want to have:

+ A **MongoDB** server that will be accessible on the localhost of our VM, in which we will store our collected data and the outputs of the machine learning tasks;
+ A **PostgresSQL** server that will support our web application data;
+ A **Flask** back-end for our application, which we will use for communicating our results to the outside world;
+ An **nginx** service to forward requests either to the Flask app or the static files;
+ Some **data-only containers** that will back-up the data from the database services.

Check out this blog post from [Real Python](https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/) which explains the process of building a muti-container application with flask, and from which we got inspired to build the docker-compose.yml file:

```yml
mongo:
  restart: always
  image: mongo:3.0.2
  volumes_from:
    - data_mongo
  ports:
    - "27017:27017"
  expose:
    - "27017"

data_mongo:
  image: mongo:3.0.2
  volumes:
    - "/vagrant/data/mongo:/var/lib/mongo:rw"
  entrypoint: "/bin/true"
```

In order to make Vagrant able to run the containers as soon it starts up, you have to provision Docker and Docker-Compose from the Vagrantfile, in which you must add the following:

```
config.vm.provision :docker
config.vm.provision :docker_compose, yml: "/vagrant/docker-compose.yml", rebuild: true, run: "always"
```

By reloading the VM this will be taken into account and the docker client will try to build our MongoDB container. If you look directly into the repository you will notice that the other containers (nginx, Flask, PostgresSQL) are also defined. However it is out of the scope of this first set-up step to explain in details how to build them.

```bash
$ vagrant reload
```

If the VM reloads successfully, it can take few minutes for Docker to set-up, you can check that the MongoDB container is effectively there. First reconnect by ssh to your VM and test your docker:

```bash
vagrant@vagrant-docker-anaconda:~$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
0c7cc8c4d3cd        mongo:3.0.2         "/entrypoint.sh mongo"   10 days ago         Up 5 hours          0.0.0.0:27017->27017/tcp   vagrant_mongo_1
```

