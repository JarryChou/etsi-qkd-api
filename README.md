The chat-demo branch is intended for demo-ing the chat app with a working QKD/qcrypto setup. This demo will work without needing to set up a web server hosting the ETSI API, as the chat app will retrieve keys directly from the qcrypto files that exists locally. As such, certain files specific to the web server are omitted in this branch.

To install just this branch, 

```
git clone --single-branch --branch chat-demo https://github.com/SpeQtral/etsi-qkd-api.git
```

Then, proceed to install the requirements. It is best to do so in a virtual environment. 
```
cd etsi-qkd-api
pip install -r requirements.txt
```

Before running the demo a few setup procedures to be done. First, we need to configure the variable ``key_file_path`` in  `config.ini`, located at ``etsi-qkd-api/api``, to point to the directory storing the qcrypto files.

Next, you need to ensure your qcrypto key files on both Alice's and Bob's machines are **identical**. They should have the same file name and the keys are identically ordered. This is necessary because the ``KME`` class that is located in ``kme.py`` reads keys from the top of the key file, which assumes they are ordered identically so both Alice and Bob retrieve the same keys.

For example, if a single 256bit key is requested by both Alice's and Bob's chat app (as is the case here), the KME class for both will simply go to ``key_file_path`` and retrieve the _first_ 8 32bit keys (concatenate 8 32bit keys = 256bit). Hence, to ensure both Alice and Bob retrieve the same 8 keys for symmetric encryption, the qcrypto files need to be identically ordered.

Once this is done, ``cd etsi-qkd-api/chat_app`` and run ``python main.py``. You should see

![mainwindow](/images/mainwindow.png)
