# Echo Client & Echo Server

TCP/IP echo client and server in python

## Getting started

### Overview

**Echo Client**

* Connects with echoserver's socket
* Receives string through stdin and sends to echoserver
* Receiving echoserver's echo is implemented as thread, so that broadcasted echo can be displayed in real-time
    * Receiving echo when sending message buffers the echo resulted by other clients

**Echo Server**

* Connects with echoclients' socket
* Receives echoclients' message and echoes it back
    * Broadcast echo if `-b` option is given

### Program Flow

1. Echoserver opens socket.
2. Echoclient opens socket and connects.
    * Each time a client connects, server initiates daemonized client thread.
4. When echoclient sends a message, echoserver displays the message to stdout and echoes it back to the server.
    * If the `-b` option is given at echoserver, message echo is broadcasted to all clients.

*Usage notification is implemented with the* `argparse` *method.*

*Multicast may be a better word choice than broadcast.*

### Development Environment

```bash
$ uname -a
Linux ubuntu 4.15.0-30-generic #32~16.04.1-Ubuntu SMP Thu Jul 26 20:25:39 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

$ python --version
Python 2.7.12
```

### Prerequisites

This program includes the following headers. Make sure you have the right packages.

Echoclient

```python
import socket
import sys
import argparse
import threading
```

Echoserver

```python
import socket
import sys
import argparse
import threading
```

Also, give executable permissions to both client and server.

```bash
$ chmod +x echoclient.py
$ chmod +x echoserver.py
```

## Running the program

### Run

**Format**

First run the server.

```bash
$ ./echoserver.py <port> [-b]
```

Then in another shell initiate client.

```bash
$ ./echoclient.py <host> <port>
```

**Example**

First run the server.

```bash
$ ./echoserver.py 1234
[+] Open port 1234
[+] Broadcast option: False

[+] Created socket
[+] Binding socket to port: 1234


```

Then in another shell initiate client.

```bash
$ ./echoclient.py 127.0.0.1 1234


Welcome to my server


```

The server shell notifies that the connection was established.

```bash
$ ./echoserver.py 1234
[+] Open port 1234
[+] Broadcast option: False

[+] Created socket
[+] Binding socket to port: 1234

[+] Connection established | IP 127.0.0.1 Port 33336


```

Now you can see that the echo works by typing messages at the client shell!

## Acknowledgements

* [Python2.7 threading module](https://docs.python.org/2/library/threading.html)
* [Python2.7 argparse module](https://docs.python.org/2/howto/argparse.html)

## Authors

* **James Sung** - *Initial work* - [sjkywalker](https://github.com/sjkywalker)
* Copyright © 2018 James Sung. All rights reserved.

