# YoutubePlayer
Play videos from YouTube directly using vlc with the ability to stream audio only. Built on Gtk 3.

<p align="center">
  <img src="/images/screenshots/screenshot1.png?raw=true" alt="YouTube Player"/>
</p>

## Features
- Minimial UI.
- Search, play and download audio or video.
- Control through mpris2.
- Music controls integrated into title bar.
- Ability to use vlc's minimal interface while playing video.

## Dependencies
- [Python 3](https://www.python.org/download/releases/3.0/)
- [Pafy](https://pypi.python.org/pypi/pafy)
- [youtube-dl](https://github.com/rg3/youtube-dl)
- [pyGObject](https://pygobject.readthedocs.io/en/latest/)
- [pydbus](https://github.com/LEW21/pydbus)

## Installation
Install the dependencies.
```bash
$ sudo apt install python3 python-pip    # For ubuntu
$ sudo pacman -S python3 python-pip      # For Arch derivatives
$ sudo -H pip install --upgrade pygobject pafy youtube-dl pydbus
```
After installing the dependencies, clone the repository and run main.py.
```bash
$ git clone https://github.com/vn-ki/YoutubePlayer.git
$ cd YoutubePlayer
$ chmod +x main.py
$ ./main.py
```

## Usage

- Enter the YouTube link in the url tab and press play. The video should start playing.
- If you want to search for the video, type ```/<search_query>``` in the url input and press play. The top search result should start playing.
- If you want to search for a playlist instead of a video, type ```//<search_query>``` in the url input and press play.
- The download feature (for now) downloads the best available quality. The downloaded file will be available in ```~/Downloads/YouTubePlayer/``` directory.
- Press the stop button to stop the running instance of vlc. Ideally this should be done before playing a new video, but is not necessary.
- The help page includes the above information.

### Known Issues

- The seek bar functions awkwardly at times.

### Upcoming features

- Improved search.
- More download options.
- Support for more players. (mpv)
- Better support for windows (Chances are thin).
- Own mpris/dbus interface.
