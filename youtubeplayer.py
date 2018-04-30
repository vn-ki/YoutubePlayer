import gi
import pafy
import json
import re
from mutagen import mp4
import urllib
import threading
import os
from time import time
from random import shuffle

##
import core.helpwindow as helpwindow
from core import util
from mpris.mpris import *
from pydbus import SessionBus
import pkg_resources
import vlc
##

ENTER = 65293
ESCAPE = 65307
RIGHT = 65363
DOWN = 65364
LEFT = 65361
UP = 65362
SPACE = 32
F11 = 65480
F12 = 65481

window = None

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gio, GLib, GObject, Notify

Notify.init('YouTube Player')

oldTime = 0
instance = vlc.Instance('--no-xlib')


class YouTubePlayer(Gtk.Window):
    def __init__(self):

        self.MINIMAL_INTERFACE = False
        self.player = instance.media_player_new()
        self.playlistThread = None
        self.ALL_SHOWN = True
        self.vidNo = 0
        self.clickCounter = 0
        self.playList = []
        self.totalTracks = 0
        self.isFullScreen = False
        self.SEARCHED = False

        self.CONFIG = {
            'AUDIO_ONLY': True,
            'VID_QUALITY': 'High',
            'AUD_QUALITY': 'High',
            'DL_VID_QUALITY': 'High',
            'DL_AUD_QUALITY': 'High'
        }

        try:
            self.CONFIG = util.readFromConfig()
        except FileNotFoundError:
            util.writeToConfig(self.CONFIG)

        Gtk.Settings.get_default().props.gtk_error_bell = False

        ##
        # Metadata

        self.title = "YouTubePlayer"
        ##
        Gtk.Window.__init__(self)
        # self.set_border_width(10)
        self.set_size_request(520, 100)

        # Title bar tweaks
        headerBar = Gtk.HeaderBar()
        headerBar.set_show_close_button(True)
        self.set_titlebar(headerBar)
        self.set_resizable(False)
        #

        ####################################################################
        # Main Box: All widgets are inside this
        superBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(superBox)
        self.mainBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.mainBox.set_property('margin', 10)
        self.mainBox.set_size_request(400, 100)

        ##

        # Video box
        self.videoEventbox = Gtk.EventBox()
        self.videoEventbox.set_property("margin", 0)
        self.videoEventbox.connect('button-press-event', self.clickOnVideo)
        self.video = Gtk.DrawingArea()
        self.video.set_size_request(500, 250)

        self.video.connect('realize', self._realized)
        self.video.connect('draw', self.onDraw)
        self.videoEventbox.add(self.video)

        superBox.pack_start(self.videoEventbox, True, True, 0)
        superBox.pack_start(self.mainBox, True, True, 0)

        ###

        # Label

        self.infoLabel = Gtk.Label("YouTubePlayer")
        self.infoLabel.set_line_wrap(True)
        self.mainBox.pack_start(self.infoLabel, True, True, 0)
        #

        # Input box
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("URL")
        self.mainBox.pack_start(self.entry, True, True, 0)

        #############################################################
        # Button for 2nd line, checkbox and download button
        #
        # Check box
        checkButtonBox = Gtk.Box(spacing=10)
        self.mainBox.pack_start(checkButtonBox, True, True, 0)
        self.audioOnlyButton = Gtk.CheckButton("With Video                   ")
        self.audioOnlyButton.connect('toggled', self.audioOnly)
        self.audioOnlyButton.set_focus_on_click(False)
        checkButtonBox.pack_start(self.audioOnlyButton, True, True, 0)

        # Download and info Box
        dliBox = Gtk.Box(spacing=10)
        dliBox.set_size_request(50, 10)
        checkButtonBox.pack_start(dliBox, True, True, 0)

        # Download button

        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="preferences-system-symbolic"),
            Gtk.IconSize.BUTTON)
        self.helpButton = Gtk.Button(image=img, name='help-button')
        self.helpButton.set_property("width-request", 30)
        self.helpButton.set_focus_on_click(False)
        self.helpButton.connect('clicked', self._showHelp)
        dliBox.pack_start(self.helpButton, True, True, 0)

        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="document-save-symbolic"), Gtk.IconSize.BUTTON)
        self.downloadButton = Gtk.Button(image=img, name='download-button')
        self.downloadButton.set_property("width-request", 30)
        self.downloadButton.set_focus_on_click(False)
        self.downloadButton.connect('clicked', self.download)
        dliBox.pack_start(self.downloadButton, True, True, 0)

        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="media-playlist-shuffle-symbolic"),
            Gtk.IconSize.BUTTON)
        self.shuffleButton = Gtk.Button(image=img)
        self.shuffleButton.set_property("width-request", 10)
        self.shuffleButton.set_focus_on_click(False)
        self.shuffleButton.connect('clicked', self.shuffle)
        dliBox.pack_start(self.shuffleButton, True, True, 0)

        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="media-playlist-repeat-symbolic"),
            Gtk.IconSize.BUTTON)
        self.repeatButton = Gtk.Button(image=img)
        self.repeatButton.set_property("width-request", 10)
        self.repeatButton.set_focus_on_click(False)
        self.repeatButton.connect('clicked', self.repeatButtonClicked)
        dliBox.pack_start(self.repeatButton, True, True, 0)

        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="system-search-symbolic"), Gtk.IconSize.BUTTON)
        self.searchButton = Gtk.Button(image=img)
        self.searchButton.set_property("width-request", 10)
        self.searchButton.set_focus_on_click(False)
        self.searchButton.connect('clicked', self.searchButtonClicked)
        dliBox.pack_start(self.searchButton, True, True, 0)

        #############################################################

        #############################################################
        # Box for lower buttons
        #

        self.buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.buttonBox.get_style_context(),
                                   "linked")

        # Previous button
        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="media-skip-backward-symbolic"),
            Gtk.IconSize.BUTTON)
        self.prevButton = Gtk.Button(image=img, name='prev-button')
        self.prevButton.connect('clicked', self.previous)
        self.prevButton.set_focus_on_click(False)
        self.buttonBox.pack_start(self.prevButton, True, True, 0)

        # Play button
        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="media-playback-start-symbolic"),
            Gtk.IconSize.BUTTON)
        self.playButton = Gtk.Button(image=img, name='play-button')
        self.playButton.connect('clicked', self.play)
        self.playButton.set_focus_on_click(False)
        self.buttonBox.pack_start(self.playButton, True, True, 0)

        # Next button
        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="media-skip-forward-symbolic"),
            Gtk.IconSize.BUTTON)
        self.nextButton = Gtk.Button(image=img, name='next-button')
        self.nextButton.connect('clicked', self.next)
        self.nextButton.set_focus_on_click(False)
        self.buttonBox.pack_start(self.nextButton, True, True, 0)

        # Show all button
        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="pan-up-symbolic"), Gtk.IconSize.BUTTON)
        self.showAllButton = Gtk.Button(image=img)
        self.showAllButton.set_focus_on_click(False)
        self.showAllButton.connect('clicked', self.showAllClicked)
        headerBar.pack_end(self.showAllButton)

        adj = Gtk.Adjustment(0.0, 0.0, 100.0, 1.0, 10.0, 10.0)

        self.currentTime = Gtk.Label("0:00")
        self.totalTime = Gtk.Label("0:00")

        self.seekBar = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, adj)
        self.seekBar.set_hexpand(True)
        self.seekBar.set_draw_value(False)
        self.seekBar.set_focus_on_click(False)
        self.seekBar.set_property("width-request", 150)
        self.seekBar.set_digits(1)
        self.seekBar.set_value(0)
        self.seekBar.connect('change-value', self.seek)

        headerBar.pack_start(self.buttonBox)
        headerBar.set_has_subtitle(False)
        headerBar.set_custom_title(self.seekBar)
        headerBar.set_decoration_layout('menu:close')
        headerBar.pack_start(self.currentTime)

        self.searchBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.searchBox.set_property('margin', 10)
        self.searchBox.set_size_request(450, -1)
        superBox.pack_start(self.searchBox, True, True, 0)
        self.searchResults = []

        self.NO_OF_SEARCH_RESULT = 5

        for i in range(self.NO_OF_SEARCH_RESULT):
            self.searchResults += [util.SearchBox()]
            self.searchBox.pack_start(self.searchResults[i], True, True, 0)

    #    seekBox.pack_start(self.seekBar, True, True, 0)
        headerBar.pack_end(self.totalTime)
        GLib.timeout_add_seconds(1, self._setSeekBar)

        ##
        self.mpris = MPRIS()
        MPRIS.dbus = pkg_resources.resource_string(
            __name__, "mpris/mpris.xml").decode("utf-8")
        self.mpris.player = self
        bus = SessionBus()
        bus.publish('org.mpris.MediaPlayer2.YouTubePlayer', self.mpris,
                    ("/org/mpris/MediaPlayer2", self.mpris))
        ##

        #############################################################

    def onDraw(self, w, cr):
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, w.get_allocated_width(), w.get_allocated_height())
        cr.fill()

    def keyPressed(self, widget, event, data=None):
        key = event.keyval
        # TODO F5 to reload

        if key == ENTER:
            self.play(None)

        elif key == SPACE:
            t = self.entry.get_text()
            if t == ' ' or t == '':
                self.entry.set_text("")
                self.play(None)

        elif key == F11:
            self.full_unfull()

        elif self.SEARCHED is True and key - 59 < 0:
            self.SEARCHED = False
            self.searchBox.hide()
            self.entry.set_text('')
            self.selectVideo(key - 49)

        elif key == LEFT:
            self._seek(self.player.get_time() - 10000)

        elif key == RIGHT:
            self._seek(self.player.get_time() + 10000)

    def selectVideo(self, vidNo):
        ytid = self.searchResults[vidNo].ytid
        t = threading.Thread(target=self.openVLC, args=[ytid])
        t.setDaemon(True)
        t.start()
        return

    def repeatButtonClicked(self, w):
        return

    def searchButtonClicked(self, w):
        if not self.SEARCHED:
            query = self.entry.get_text()

            if query[0] == '/':
                fun = util._getYTResultURL
                query = query[1:]
                if query[0] == '/':
                    fun = util._getYTResultURL_PL
                    query[1:]

            results = fun(query)

            for i in range(self.NO_OF_SEARCH_RESULT):
                self.searchResults[i].setTitleAndId(
                    str(i + 1) + ': ' + results[i]['title'], results[i]['id'])

            self.searchBox.show()
            self.SEARCHED = True

            return

        else:
            self.searchBox.hide()
            self.SEARCHED = False

    def show(self):
        self.show_all()
        self.seekBar.hide()
        self.currentTime.hide()
        self.totalTime.hide()
        self.videoEventbox.hide()
        self.searchBox.hide()

    def showAllClicked(self, widget):
        if self.ALL_SHOWN:
            img = Gtk.Image.new_from_gicon(
                Gio.ThemedIcon(name="pan-down-symbolic"), Gtk.IconSize.BUTTON)
            widget.set_image(img)
            self.mainBox.hide()
            self.searchBox.hide()
            self.ALL_SHOWN = False
        else:
            img = Gtk.Image.new_from_gicon(
                Gio.ThemedIcon(name="pan-up-symbolic"), Gtk.IconSize.BUTTON)
            widget.set_image(img)
            self.mainBox.show()
            self.ALL_SHOWN = True
            if self.CONFIG['AUDIO_ONLY']:
                self.videoEventbox.hide()

    def clickOnVideo(self, widget, event):
        global oldTime
        if time() - oldTime < 0.2:
            self.full_unfull()
        oldTime = time()

    def full_unfull(self):
        if self.isFullScreen:
            self.unfullscreen()
            self.isFullScreen = False
            if self.ALL_SHOWN:
                self.mainBox.show()
        else:
            self.mainBox.hide()
            self.searchBox.hide()
            self.fullscreen()

            # self.video.emit('draw')
            self.isFullScreen = True

    def play(self, widget):
        url = self.entry.get_text()
        if url == '':  # ERROR Check ! isPlaying()
            state = self.player.get_state()

            if state == vlc.State.Paused:
                img = Gtk.Image.new_from_gicon(
                    Gio.ThemedIcon(name="media-playback-pause-symbolic"),
                    Gtk.IconSize.BUTTON)
                self.player.play()
                self.playButton.set_image(img)
                self.mpris.PlaybackStatus = "Playing"
                self.mpris.Rate = 1.0
                self.mpris.Position = self.player.get_time() * 1000
            elif state == vlc.State.Playing:
                img = Gtk.Image.new_from_gicon(
                    Gio.ThemedIcon(name="media-playback-start-symbolic"),
                    Gtk.IconSize.BUTTON)
                self.player.pause()
                self.playButton.set_image(img)
                self.mpris.PlaybackStatus = "Paused"
                self.mpris.Rate = 0.0
                self.mpris.Position = self.player.get_time() * 1000
            else:
                self.infoLabel.set_text("URL field is empty.")
            return

        self.clickCounter = 1

        t = threading.Thread(target=self.openVLC, args=[url])
        t.setDaemon(True)
        t.start()
        return

    def openVLC(self, url):

        # Check if input is a url or search query
        search_query = url

        if url[0] == '/':  # search term
            if url[1] == '/':
                # Search for playlist
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Searching for playlist",
                    priority=GObject.PRIORITY_DEFAULT)
                url = util._getYTResultURL_PL(url[2:])[0]['id']
                if url == -1:  # Error loading url
                    return
            else:
                # Search for video
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Searching for video",
                    priority=GObject.PRIORITY_DEFAULT)
                url = util._getYTResultURL(url[1:])[0]['id']
                if url == -1:  # Error loading url
                    return

        if 'list' not in url and url[:2] != 'PL':  # not a playlist
            try:
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Playing",
                    priority=GObject.PRIORITY_DEFAULT)
                vid = pafy.new(url)
                if search_query[-4:] == '/mix':
                    playlist = vid.mix
                    print(playlist['title'])
                    self.totalTracks = len(playlist['items'])
                    GObject.idle_add(
                        self.infoLabel.set_text,
                        playlist['title'],
                        priority=GObject.PRIORITY_DEFAULT)
                    self.playList = playlist['items']
                    self._playPlaylist()
                else:
                    self._openVLCShell(vid)
            except ValueError:
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Use /<search_query>. Don't ask me why. XD",
                    priority=GObject.PRIORITY_DEFAULT)
                return
            except Exception as e:
                print(e)
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Error getting video",
                    priority=GObject.PRIORITY_DEFAULT)
                return

        else:  # A playlist
            try:
                playlist = pafy.get_playlist(url)
            except ValueError:
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Use //<search_query>. Don't ask me why. XD",
                    priority=GObject.PRIORITY_DEFAULT)
                return
            except:
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Error getting playlist",
                    priority=GObject.PRIORITY_DEFAULT)
                return
            self.totalTracks = len(playlist['items'])
            GObject.idle_add(
                self.infoLabel.set_text,
                playlist['title'],
                priority=GObject.PRIORITY_DEFAULT)
            self.playList = playlist['items']
            self._playPlaylist()

    def _realized(self, widget, data=None):
        self.windowID = widget.get_window().get_xid()

    def _playPlaylist(self):
        try:
            video = self.playList[self.vidNo]['pafy']
        except Exception as e:
            print(e)
            return
        self._openVLCShell(video)

    def _openVLCShell(self, video):

        metadata = self._getMetadata(video)
        self.length = video.length
        self.totalTime.set_text(self._secondsToTime(self.length))

        if metadata is None:
            GObject.idle_add(
                self.infoLabel.set_text,
                video.title,
                priority=GObject.PRIORITY_DEFAULT)
            self.mpris.Metadata = {
                'xesam:title':
                GLib.Variant('s', video.title),
                'mpris:trackid':
                GLib.Variant('o', '/org/mpris/MediaPlayer2/YouTubePlayer/' +
                             str(self.vidNo)),
                'mpris:length':
                GLib.Variant('x', video.length * 1000000),
                'mpris:artUrl':
                GLib.Variant('s', video.thumb)
            }

        else:
            GObject.idle_add(
                self.infoLabel.set_text,
                metadata['track_title'] + ' - ' + metadata['artist'],
                priority=GObject.PRIORITY_DEFAULT)
            self.mpris.Metadata = {
                'xesam:title':
                GLib.Variant('s', metadata['track_title']),
                'mpris:trackid':
                GLib.Variant('o', '/org/mpris/MediaPlayer2/YouTubePlayer/' +
                             str(self.vidNo)),
                'mpris:length':
                GLib.Variant('x', video.length * 1000000),
                'mpris:artUrl':
                GLib.Variant('s', metadata['album_art_url']),
                'xesam:album':
                GLib.Variant('s', metadata['album']),
                'xesam:artist':
                GLib.Variant('as', [metadata['artist']])
            }

        if self.CONFIG['AUDIO_ONLY'] is True:
            GObject.idle_add(
                self.set_resizable, False, priority=GObject.PRIORITY_DEFAULT)
            GObject.idle_add(self.videoEventbox.hide)
            # self.showAllButton.hide()
            try:
                if self.CONFIG['AUD_QUALITY'] == 'High':
                    audio_url = video.getbestaudio().url
                elif self.CONFIG['AUD_QUALITY'] == 'Medium':
                    audio_url = video.audiostreams[len(video.audiostreams) //
                                                   2].url
                elif self.CONFIG['AUD_QUALITY'] == 'Low':
                    audio_url = video.audiostreams[0].url
            except OSError:
                # Error retrieving the video
                # TODO Retry 3 times on receving error
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Can't play the requested video",
                    priority=GObject.PRIORITY_DEFAULT)
                if self.vidNo != self.totalTracks:
                    self.next(None)
                return
            self.player.set_mrl(audio_url)
            self.player.play()

        else:
            GObject.idle_add(
                self.set_resizable, True, priority=GObject.PRIORITY_DEFAULT)
            try:
                if self.CONFIG['VID_QUALITY'] == 'High':
                    video_url = video.getbest().url
                elif self.CONFIG['VID_QUALITY'] == 'Medium':
                    video_url = video.streams[len(video.streams) // 2].url
                elif self.CONFIG['VID_QUALITY'] == 'Low':
                    video_url = video.streams[1].url
            except OSError:
                if self.vidNo != self.totalTracks:
                    self.next(None)
                GObject.idle_add(
                    self.infoLabel.set_text,
                    "Can't play the requested video",
                    priority=GObject.PRIORITY_DEFAULT)
                return
            # TODO
            self.player.set_xwindow(self.windowID)
            self.player.video_set_mouse_input(False)
            GObject.idle_add(self.videoEventbox.show)
            self.player.set_mrl(video_url)
            self.player.play()

        if not self.is_active() and metadata is not None:
            icon_path = os.path.realpath('images/icons/yt-icon.png')
            Notify.Notification.new(
                metadata['track_title'],
                metadata['album'] + '\n' + metadata['artist'],
                icon_path).show()

        self.player.audio_set_volume(100)
        GObject.idle_add(self.currentTime.show)
        GObject.idle_add(self.seekBar.show)
        GObject.idle_add(self.totalTime.show)
        self.mpris.PlaybackStatus = "Playing"
        self.mpris.Rate = 1.0
        img = Gtk.Image.new_from_gicon(
            Gio.ThemedIcon(name="media-playback-pause-symbolic"),
            Gtk.IconSize.BUTTON)
        GObject.idle_add(
            self.playButton.set_image, img, priority=GObject.PRIORITY_DEFAULT)
        GObject.idle_add(
            self.entry.set_text, "", priority=GObject.PRIORITY_DEFAULT)

    def next(self, widget):
        if self.vidNo != self.totalTracks:
            self.player.stop()

            self.vidNo += 1
            thread = threading.Thread(target=self._playPlaylist)
            thread.setDaemon(True)
            thread.start()

        else:
            self.infoLabel.set_text('All songs have been played')
            self.mpris.PlaybackStatus = "Stopped"

    def previous(self, widget):
        if self.vidNo != 0:
            self.vidNo -= 1
            self._playPlaylist()

    def seek(self, sc, value, ud):
        # WTF TODO
        seek = self.seekBar.get_value()
        self._seek(int(ud * self.length * 10))

    def _seek(self, absSeek):
        self.player.set_time(absSeek)
        self.mpris.Position = self.player.get_time() * 1000
        self.mpris.Seeked(self.mpris.Position)

    def download(self, widget):
        url = self.entry.get_text()
        thread = threading.Thread(target=self._download, args=[url])
        thread.setDaemon(True)
        thread.start()

    def _download(self, url):
        if url == '':
            self.infoLabel.set_text("I can't download nothing. XD")
            return

        if url[0] == '/':  # search term
            if url[1] == '/':
                # Search for playlist
                self.infoLabel.set_text("Searching for playlist")
                url = util._getYTResultURL_PL(url[2:])[0]['id']
                if url == -1:  # Error finding url
                    return
            else:
                # Search for video
                self.infoLabel.set_text("Searching for video")
                url = util._getYTResultURL(url[1:])[0]['id']
                if url == -1:  # Error finding url
                    return

        if 'list=' not in url:
            video = pafy.new(url)

            if self.CONFIG['AUDIO_ONLY'] is True:
                self._downloadAudio(video)

            else:
                self._downloadVideo(video)
            return

        else:
            # download using youtube-dl
            pass
        return

    def _setdownloadETA(self, a, b, percentage, d, ETA):
        GObject.idle_add(
            self.infoLabel.set_text,
            'Completed : ' + str(int(percentage * 100)) + '% ETA : ' +
            str(int(ETA)) + 's',
            priority=GObject.PRIORITY_DEFAULT)
        GObject.idle_add(
            self.entry.set_progress_fraction,
            percentage,
            priority=GObject.PRIORITY_DEFAULT)

    def _downloadAudio(self, video):
        filepath = os.environ.get(
            'HOME') + '/Downloads/YouTubePlayer/' + video.title + '[audio].m4a'
        audio = video.m4astreams[-1]
        try:
            audio.download(
                filepath, quiet=False, callback=self._setdownloadETA)
        except FileNotFoundError:
            os.makedirs(os.environ.get('HOME') + '/Downloads/YouTubePlayer')
            audio.getbestaudio(preftype="m4a").download(
                filepath, quiet=False, callback=self._setdownloadETA)

        metadata = self._getMetadata(video)
        if metadata is None:
            return

        self.infoLabel.set_text('Fixing metadata')
        audiofile = mp4.MP4(filepath)

        audiofile['\xa9nam'] = metadata['track_title']
        audiofile['\xa9ART'] = metadata['artist']
        audiofile['\xa9alb'] = metadata['album']
        audiofile['aART'] = metadata['artist']

        cover = metadata['album_art_url']
        fd = urllib.request.urlopen(cover)
        covr = mp4.MP4Cover(fd.read(),
                            getattr(mp4.MP4Cover, 'FORMAT_PNG' if
                                    cover.endswith('png') else 'FORMAT_JPEG'))
        fd.close()
        audiofile['covr'] = [covr]
        audiofile.save()
        self.infoLabel.set_text('Metadata fixed')

    def _downloadVideo(self, video):
        try:
            video.getbest(preftype="mp4").download(
                filepath=os.environ.get('HOME') + '/Downloads/YouTubePlayer/' +
                video.title + '.' + video.getbest().extension,
                quiet=False,
                callback=self._setdownloadETA)
        except FileNotFoundError:
            os.makedirs(os.environ.get('HOME') + '/Downloads/YouTubePlayer')
            video.getbest(preftype="mp4").download(
                filepath=os.environ.get('HOME') + '/Downloads/YouTubePlayer/' +
                video.title + '.' + video.getbest().extension,
                quiet=False,
                callback=self._setdownloadETA)

    def audioOnly(self, widget):
        self.CONFIG['AUDIO_ONLY'] = not widget.get_active()
        return

    def _showHelp(self, widget):

        global window

        # if window == None :
        window = helpwindow.helpWindow()
        window.set_modal(self)
        window.set_transient_for(self)
        window.set_destroy_with_parent(True)
        window.connect("delete-event", window.buttonClicked)
        window.show_function()
        # Gtk.main()
        return

    def shuffle(self, widget):
        shuffle(self.playList)

    def _setSeekBar(self):
        if self.player.get_state() != vlc.State.NothingSpecial:
            currentTime = self.player.get_time() // 1000
            if currentTime == self.length - 1:
                self.next(None)

            GObject.idle_add(
                self.currentTime.set_text,
                self._secondsToTime(currentTime),
                priority=GObject.PRIORITY_DEFAULT)
            GObject.idle_add(
                self.seekBar.set_value,
                int((float(currentTime) / self.length) * 100),
                priority=GObject.PRIORITY_DEFAULT)

        return True

    def _secondsToTime(self, seconds):
        t = ''
        t += str(int(seconds / 60))
        t += ':'
        if seconds % 60 < 10:
            t += '0' + str(seconds % 60)

        else:
            t += str(seconds % 60)
        return t

    def _getMetadata(self, video):
        t = re.sub("[\(\[].*?[\)\]]", "", video.title.lower())
        t = t.split('-')

        if len(
                t
        ) != 2:  # If len is not 2, no way of properly knowing title for sure
            t = t[0]
            t = t.split(':')
            if len(
                    t
            ) != 2:  # Ugly, but to be safe in case all these chars exist, Will improve
                t = t[0]
                t = t.split('|')
                if len(t) != 2:
                    return None

        t[0] = re.sub("(ft |ft.|feat |feat.).*.", "", t[0])
        t[1] = re.sub("(ft |ft.|feat |feat.).*.", "", t[1])

        t[0] = t[0].strip()
        t[1] = t[1].strip()

        metadata = self._getMetadataFromLastfm(t[0], t[1])

        if metadata is None:
            return metadata

        metadata = self._getMetadataFromLastfm(t[1], t[0])
        return metadata

    def _getMetadataFromLastfm(self, artist, track):

        url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=12dec50313f885d407cf8132697b8712&'
        url += urllib.parse.urlencode({"artist": artist}) + '&'
        url += urllib.parse.urlencode({"track": track}) + '&'
        url += '&format=json'

        resp = urllib.request.urlopen(url)

        metadata = dict()

        data = json.loads(resp.read())

        if 'track' != list(data.keys())[0]:
            return None
        try:
            metadata['track_title'] = data['track']['name']
            metadata['artist'] = data['track']['artist']['name']
            metadata['album'] = data['track']['album']['title']
            metadata['album_art_url'] = data['track']['album']['image'][-1][
                '#text']
        except:
            return None

        return metadata
