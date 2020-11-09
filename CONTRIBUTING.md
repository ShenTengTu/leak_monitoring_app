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
- See "[Install Docker Engine on Ubuntu]" for Ubuntu.
- See "[Install Docker Engine on Debian]" for Raspbian.

[Install Docker Engine on Ubuntu]: https://docs.docker.com/engine/install/ubuntu/
[Install Docker Engine on Debian]: https://docs.docker.com/engine/install/debian/
