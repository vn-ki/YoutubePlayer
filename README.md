# YoutubePlayer
Play videos from YouTube directly using vlc with the ability to stream audio only.

## Dependencies
- [Python 3](https://www.python.org/download/releases/3.0/)
- [Pafy](https://pypi.python.org/pypi/pafy)
- [youtube-dl](https://github.com/rg3/youtube-dl) (Optional, highly recomended)

## Installation
Install the dependencies.
```bash
$ sudo apt install python3 python-pip    # For ubuntu
$ sudo pacman -S python3 python-pip      # For Arch derivatives
$ sudo -H pip install --upgrade pygobject pafy youtube-dl
```
After installing the dependencies, clone the repository and run main.py.
```bash
$ git clone https://github.com/vn-ki/YoutubePlayer.git
$ cd YoutubePlayer
$ chmod +x main.py
$ ./main.py
```
