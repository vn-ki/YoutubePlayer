# YoutubePlayer
Play videos from YouTube directly using vlc with the ability to stream audio only.

<p align="center">
  <img src="/images/screenshots/screenshot1.png?raw=true" alt="YouTube Player"/>
</p>

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

## Usage

- Enter the YouTube link in the url tab and press play. The video should start playing.
- If you want to search for the video, type ```/<search_query>``` in the url input and press play. The top search result should start playing.
- If you want to search for a playlist instead of a video, type ```//<search_query>``` in the url input and press play.
- The download feature (for now) downloads the best available quality. The downloaded file will be available in ```~/Downloads/YouTubePlayer/``` directory.

## Upcoming features

- Better support for windows.
- Improved search
- More download options
