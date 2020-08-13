## Introduction

The chat-demo branch is intended for demo-ing the chat app with a working QKD/qcrypto setup. This demo will work without needing to set up a web server hosting the ETSI API, as the chat app will retrieve keys directly from the qcrypto files that exists locally. As such, certain files specific to the web server are omitted in this branch. We will call Alice and Bob the two parties trying to chat with each other in this demo. 

## Easy Installation

The easy installation involves downloading an Ubuntu 18.04 image preloaded with the Git branch and relevant software dependencies. Go to the SharePoint at this [link](https://speqtralquantum.sharepoint.com/:f:/s/technical/Em0XzC4ro7hHm6wWVxA_HxUBp1MkmHev0GZBAuziFKTkGA?e=UoTShF) and download the .ovf file.

Assuming you are using VirtualBox, go to File > Import Appliance and import the .ovf. The account and password for the Ubuntu image is 'test' and '123' respectively. Once you are inside Ubuntu, fire up the terminal

```
cd etsi-qkd-api
source venv/bin/activate
cd chat_app
python main.py
```
and the connection window should appear. You can obtain the IP of this VM in your terminal with the ``ifconfig`` command.

## Manual Installation from Git Repository

This is if you would like to install it onto your own system. To install just this branch, 

```
git clone --single-branch --branch chat-demo https://github.com/SpeQtral/etsi-qkd-api.git
```

Then, proceed to install the requirements. It is best to do so in a virtual environment. This tutorial will assume an Ubuntu 18.04 installation (on other Ubuntu versions you may face some issues due to the different Python version bundled with the OS).
```
cd etsi-qkd-api
python3 -m venv venv
sudo apt-get install qt5-default
source venv/bin/activate
pip install -r requirements.txt
```

The app uses the [Qt5](https://www.qt.io) software to code the GUI. You may find that during installation of requirements there are some errors regarding missing ``wheel`` dependencies. The chat app still works without these dependencies so it does not seem to be an issue. Now we are done with installation and we can proceed with configuring the chat app. 

## Setup

First, there are two ports that are used in this app, shown in ``chat_app/port_config.ini``, one for establishing connection with your partner and one for sending encrypted messages. The defaults are ``6180`` and ``6190`` respectively, but feel free to change them in this file. You would probably have to do so for port forwarding if your two PCs are not on the same local network. Otherwise, if they are on the same network then the default should work.

Secondly, we need to configure the variable ``key_file_path`` in  ``config.ini``, located at ``etsi-qkd-api/api``, to point to the directory storing the qcrypto files. 

You need to ensure your qcrypto key files on both Alice's and Bob's machines are **identical**. They should have the same file name and the keys are identically ordered. This is necessary because the ``KME`` class that is located in ``kme.py`` reads keys from the top of the key file, which assumes they are ordered identically so both Alice and Bob retrieve the same keys.

For example, if a single 256bit key is requested by both Alice's and Bob's chat app (as is the case here), the KME class for both will simply go to ``key_file_path`` and retrieve the _first_ eight 32bit keys (8 x 32bit keys = 256bit). Hence, to ensure both Alice and Bob retrieve the same 8 keys for symmetric encryption, the qcrypto files need to be identically ordered.

## Run

Once you are done with the setup, ``cd etsi-qkd-api/chat_app`` and run ``python main.py`` on both Alice and Bob. You should see

![connectwindow](/images/connectwindow.png)

Proceed to key in the IP address of the other party's PC and a username for the chat before clicking a Connect. A background worker thread will check for outgoing/incoming connections. When a succesful connection is established, the chat interface will appear

![chattwindow](/images/chatwindow.png)

The chat interface consists of three main panes. The bottom pane is for composing your message. Upon sending your message, the encrypted version which is sent to the other party appears on the encrypted chat pane, while the decrypted message appears on the left pane. AES256 is used to encrypt the entire chat session. If you have your qcrypto key files correctly configured, the chat app should work as intended on both Alice and Bob. Otherwise, you might find that the messages are not properly decrypted on either end. 
