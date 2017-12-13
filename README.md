# YoutubePlayer
Search and play videos from YouTube directly with the ability to stream audio only. Download video or audio from youtube directly. Song metadata including album art is automatically fixed when you stream or download a song.

<p align="center">
  <img src="/images/screenshots/screenshot1.png?raw=true" alt="YouTube Player"/>
  <img src="/images/screenshots/screenshot2.png?raw=true" alt="YouTube Player"/>
</p>
<p align="center">
  <img src="/images/screenshots/screenshot3.png?raw=true" alt="YouTube Player"/>
</p>


## Features
- Minimial UI.
- Search, play and download audio or video.
- Auto correction of metadata (from last.fm) whenever possible.
- Control through mpris.
- Music controls integrated into title bar.

## Dependencies
- [Python 3](https://www.python.org/download/releases/3.0/)
- [libvlc](https://github.com/oaubert/python-vlc)
- [Pafy](https://pypi.python.org/pypi/pafy)
- [youtube-dl](https://github.com/rg3/youtube-dl)
- [pyGObject](https://pygobject.readthedocs.io/en/latest/)
- [pydbus](https://github.com/LEW21/pydbus)
- [mutagen](http://mutagen.readthedocs.io/en/latest/index.html)

## Installation
Install the dependencies.
```bash
$ sudo apt install python3 python-pip    # For ubuntu
$ sudo pacman -S python3 python-pip      # For Arch derivatives
$ sudo -H pip install --upgrade pygobject python-vlc pafy youtube-dl pydbus mutagen
```
After installing the dependencies, clone the repository and run main.py.
```bash
$ git clone https://github.com/vn-ki/YoutubePlayer.git
$ cd YoutubePlayer
$ chmod +x YouTubePlayer
$
$ # Installation
$ ./YouTubePlayer install
$
$ # Uninstallation
$ ./YouTubePlayer uninstall
$
$ # Demo Run
$ ./YouTubePlayer run
```



## Usage

- Enter the YouTube link in the url tab and press play. The video should start playing.
- If you want to search for the video, type ```/<search_query>``` in the url input and press play. The top search result should start playing.
- If you want to search for a playlist instead of a video, type ```//<search_query>``` in the url input and press play.
- The download feature (for now) downloads the best available quality. The downloaded file will be available in ```~/Downloads/YouTubePlayer/``` directory.
- Press the stop button to stop the running instance of vlc. Ideally this should be done before playing a new video, but is not necessary.
- The help page includes the above information.

### Upcoming features

- Improved search.
- More download options.
- Better support for windows (Chances are thin).
