# Development guide
The development enviroment of the project only support Linux only.

## Python
We use **[pyenv]** to manage Python version, and This project use **Python 3.7.9**.

### Python dependency management
This project use **[Poetry]** to manage dependencyies.

[pyenv]: https://github.com/pyenv/pyenv
[Poetry]: https://python-poetry.org/docs/

## Node.js
We use **[fnm]** to manage Node.js version and This project use **Node.js 14.15.1**.

### Node.js dependency management
This project use **[Yarn]** to manage dependencyies.

```
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -

echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

sudo apt update

sudo apt remove cmdtest

sudo apt-get install --no-install-recommends yarn
```
>  Ubuntu 17.04 comes with cmdtest installed by default. If you’re getting errors from installing yarn, you may want to run `sudo apt remove cmdtest` first.

[fnm]: https://github.com/Schniz/fnm
[Yarn]: https://classic.yarnpkg.com/en/docs/install#debian-stable

## Docker
The application of this project runs in **Docker containers**.
- See "[Install Docker Engine on Ubuntu]" for Ubuntu. **(version 19.03.14)**
- See "[Install Docker Engine on Debian]" for Raspbian. **(version 19.03.14)**

## Docker Compose
The application of this project runs in **Docker containers**.
- See "[Install Docker Compose (Linux)]"for Ubuntu. **(version 1.27.4)**
- See "[Install Docker Compose (Alternative Install Options)]"for Raspbian. **(version 1.27.4)**

Installing Docker Compose on Raspbian needs using `pip`.

### For development on Raspbian
Because We use **[pyenv]** to manage Python version,
please  using **3.7.9** version in **global** scope.
```
$ pyenv global 3.7.9

$ pyenv versions
  system
* 3.7.9 (set by /home/pi/.pyenv/version)

$ python -- version
Python 3.7.9
```

Then, install dependencies first.
```
$ sudo apt-get install -y libffi-dev libssl-dev
$ sudo apt-get remove python-configparser
```

At last, install Docker Compose from pypi using `pip`, and reload shell after installing successful.
```
$ pip install docker-compose

$ source ~/.profile
```

Check the installation path.
```
$ which docker-compose
/home/pi/.pyenv/shims/docker-compose

$ pyenv which docker-compose
/home/pi/.pyenv/versions/3.7.9/bin/docker-compose
```

### For deployment  on Raspbian
Install dependencies first.
```
$ sudo apt-get install -y libffi-dev libssl-dev
$ sudo apt-get remove python-configparser
```

Using system `pip3` to install Docker Compose.
```
$ sudo pip3 -v install docker-compose
```

Check the installation path.
```
$ sudo which docker-compose
/usr/local/bin/docker-compose
```


[Install Docker Engine on Ubuntu]: https://docs.docker.com/engine/install/ubuntu/
[Install Docker Engine on Debian]: https://docs.docker.com/engine/install/debian/
[Install Docker Compose (Linux)]: https://docs.docker.com/compose/install/#install-compose-on-linux-systems
[Install Docker Compose (Alternative Install Options)]: https://docs.docker.com/compose/install/#alternative-install-options
