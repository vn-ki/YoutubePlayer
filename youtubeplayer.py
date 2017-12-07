import gi
import subprocess
import pafy
import urllib
import threading
import os
from time import sleep

import helpwindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class YouTubePlayer(Gtk.Window) :
    def __init__(self) :

        self.AUDIO_ONLY = False
        self.MINIMAL_INTERFACE = True
        self.vlcShell = None
        self.downloadThread = None
        self.playlistThread = None
        self.playlistNames = []
        self.vidNo = 0


        Gtk.Window.__init__(self, title="YouTubePlayer")
        self.set_border_width(10)
        self.set_size_request(500, 100)

        #Title bar tweaks
        headerBar = Gtk.HeaderBar()
        headerBar.set_show_close_button(True)
        headerBar.props.title = ""
        self.set_titlebar(headerBar)
        #

        ####################################################################
        ## Main Box: All widgets are inside this
        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        ##

        #Label

        self.infoLabel = Gtk.Label("YouTubePlayer")
        mainBox.pack_start(self.infoLabel, True, True, 0)
        #

        #Input box
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("URL")
        mainBox.pack_start(self.entry, True, True, 0)


        #############################################################
        #Button for 2nd line, checkbox and download button
        #
        #Check box
        checkButtonBox = Gtk.Box(spacing=10)
        mainBox.pack_start(checkButtonBox, True, True, 0)
        self.audioOnlyButton = Gtk.CheckButton("Audio only")
        self.audioOnlyButton.connect('toggled', self.audioOnly)
        checkButtonBox.pack_start(self.audioOnlyButton, True, True,0)

        self.mininalInterfaceButton = Gtk.CheckButton("Minimal Interface")
        self.mininalInterfaceButton.set_active(True)
        self.mininalInterfaceButton.connect('toggled', self._mininalInterface)
        checkButtonBox.pack_start(self.mininalInterfaceButton, True, True,0)

        #Download and info Box
        dliBox = Gtk.Box(spacing=10)
        checkButtonBox.pack_start(dliBox, True, True, 0)

        #Download button
        img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="document-save-symbolic"), Gtk.IconSize.BUTTON)
        self.downloadButton = Gtk.Button( image=img, name='download-button')
        self.downloadButton.set_property("width-request", 30)
        self.downloadButton.connect('clicked', self.download)
        dliBox.pack_start(self.downloadButton, True,True,0)

        img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-stop-symbolic"), Gtk.IconSize.BUTTON)
        self.downloadButton = Gtk.Button( image=img, name='quitvlc-button')
        self.downloadButton.set_property("width-request", 30)
        self.downloadButton.connect('clicked', self._quitVLC)
        dliBox.pack_start(self.downloadButton, True,True,0)

        img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="help-about-symbolic"), Gtk.IconSize.BUTTON)
        self.downloadButton = Gtk.Button( image=img, name='help-button')
        self.downloadButton.set_property("width-request", 30)
        self.downloadButton.connect('clicked', self._showHelp)
        dliBox.pack_start(self.downloadButton, True,True,0)
        #############################################################

        #############################################################
        #Box for lower buttons
        #

        self.buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.buttonBox.get_style_context(), "linked")
        self.add(mainBox)

        #Previous button
        img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-skip-backward-symbolic"), Gtk.IconSize.BUTTON)
        self.prevButton = Gtk.Button(image=img, name='prev-button')
        self.prevButton.connect('clicked', self.previous)
        self.buttonBox.pack_start(self.prevButton, True, True, 0)

        #Play button
        img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-start-symbolic"), Gtk.IconSize.BUTTON)
        self.playButton = Gtk.Button(image=img, name='play-button')
        self.playButton.connect('clicked', self.play)
        self.buttonBox.pack_start(self.playButton, True, True, 0)

        #Next button
        img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-skip-forward-symbolic"), Gtk.IconSize.BUTTON)
        self.nextButton = Gtk.Button(image=img, name='next-button')
        self.nextButton.connect('clicked', self.next)
        self.buttonBox.pack_start(self.nextButton, True, True, 0)

        headerBar.pack_start(self.buttonBox)
        #############################################################

    def play(self, widget) :
        url = self.entry.get_text()

        if self.vlcShell != None :
            self.vlcShell.stdin.write(bytes('status\n', 'utf-8'))
            try :
                self.vlcShell.stdin.flush()
                x = ''
                for x in iter(self.vlcShell.stdout.readline, b''):
                    x = str(x, 'utf-8')
                    if 'state' in x :
                        break
                x = x.split(' ')
                if x[2] == 'playing' :
                    img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-start-symbolic"), Gtk.IconSize.BUTTON)
                    self.vlcShell.stdin.write(bytes('pause\n', 'utf-8'))
                    self.playButton.set_image(img)

                elif x[2]=='stopped':
                    self.vlcShell.stdin.write(bytes('q\n', 'utf-8'))

                else :
                    img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-pause-symbolic"), Gtk.IconSize.BUTTON)
                    self.vlcShell.stdin.write(bytes('pause\n', 'utf-8'))
                    self.playButton.set_image(img)

                self.vlcShell.stdin.flush()
                return
            except BrokenPipeError:
                self.vlcShell = None

        if url == '' :
            self.infoLabel.set_text("URL field is empty.")
            return

        img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-pause-symbolic"), Gtk.IconSize.BUTTON)
        self.playButton.set_image(img)

        self.openVLC(url)
        return

    def openVLC(self,url) :

        if url[0] == '/' : # search term
            if url[1] == '/' :
                # Search for playlist
                self.infoLabel.set_text("Searching for playlist")
                url = self._getFirstYTResultURL_PL(url[2:])
            else :
                #Search for video
                self.infoLabel.set_text("Searching for video")
                url = self._getFirstYTResultURL(url[1:])

        if 'list=' not in url: #not a playlist
            vid = pafy.new(url)



            self._openVLCShell(vid)
        else: # A playlist
            playlist = pafy.get_playlist(url)
            self.infoLabel.set_text(playlist['title'])
            self._playPlaylist(playlist)


    def next(self, widget) :
        try :
            self.vlcShell.stdin.write(bytes('next\n', 'utf-8'))
            self.vlcShell.stdin.flush()
            self.vidNo += 1
            try :
                self.infoLabel.set_text(self.playlistNames[self.vidNo])
            except :
                return

        except AttributeError :
            self.infoLabel.set_text("Play something first.")
        return

    def previous(self, widget):
        try :
            self.vlcShell.stdin.write(bytes('prev\n', 'utf-8'))
            self.vlcShell.stdin.flush()
            self.vidNo -= 1
            try :
                self.infoLabel.set_text(self.playlistNames[self.vidNo])
            except :
                return

        except AttributeError :
            self.infoLabel.set_text("Play something first.")
        return

    def download(self, widget) :
        #must use threading
        url = self.entry.get_text()

        if url[0] == '/' : # search term
            if url[1] == '/' :
                # Search for playlist
                self.infoLabel.set_text("Searching for playlist")
                url = self._getFirstYTResultURL_PL(url[2:])
            else :
                #Search for video
                self.infoLabel.set_text("Searching for video")
                url = self._getFirstYTResultURL(url[1:])

        if url == '' :
            self.infoLabel.set_text("I can't download nothing. XD")
            return
        if 'list=' not in url:
            video = pafy.new(url)


            if self.AUDIO_ONLY == True :
                self.downloadThread = threading.Thread(target=self._downloadAudio, args=[video])
                self.downloadThread.start()

            else:
                self.downloadThread = threading.Thread(target=self._download, args=[video])
                self.downloadThread.start()
            return

        else:
            # download using youtube-dl
            pass
        return

    def _setdownloadETA(self, a, b, percentage, d, ETA) :
        self.infoLabel.set_text('Completed : '+str(int(percentage*100))+' ETA : '+str(int(ETA))+'s')
        self.entry.set_progress_fraction(percentage)
        
    def _downloadAudio(self, video) :
        try :
            video.getbestaudio().download(filepath=os.environ.get('HOME')+'/Downloads/YouTubePlayer/'+video.title+'[audio].'+video.getbestaudio().extension, quiet=False, callback=self._setdownloadETA)
        except FileNotFoundError :
            os.makedirs(os.environ.get('HOME')+'/Downloads/YouTubePlayer')
            video.getbestaudio().download(filepath=os.environ.get('HOME')+'/Downloads/YouTubePlayer/'+video.title+'[audio].'+video.getbestaudio().extension, quiet=False, callback=self._setdownloadETA)

    def _download(self, video) :
        try :
            video.getbest(preftype="mp4").download(filepath=os.environ.get('HOME')+'/Downloads/YouTubePlayer/'+video.title+'.'+video.getbest().extension, quiet=False, callback=self._setdownloadETA)
        except FileNotFoundError :
            os.makedirs(os.environ.get('HOME')+'/Downloads/YouTubePlayer')
            video.getbest(preftype="mp4").download(filepath=os.environ.get('HOME')+'/Downloads/YouTubePlayer/'+video.title+'.'+video.getbest().extension, quiet=False, callback=self._setdownloadETA)

    def audioOnly(self, widget) :
        self.AUDIO_ONLY = widget.get_active()
        if self.AUDIO_ONLY:
            self.mininalInterfaceButton.set_sensitive(False)
        else :
            self.mininalInterfaceButton.set_sensitive(True)
        return

    def _getFirstYTResultURL(self, query)  :
        query_string = urllib.parse.urlencode({"search_query" : query})
        response = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        html_content=response.read().decode(response.headers.get_content_charset())
        i = str(html_content).index("watch?")
        search_results = html_content[i+8: i+19]
        return search_results

    def _getFirstYTResultURL_PL(self, query) :
        query_string = urllib.parse.urlencode({"search_query" :  'playlist ' + query})
        response = urllib.request.urlopen("https://www.youtube.com/results?" + query_string + "&sp=EgIQAw%253D%253D")
        html_content=response.read().decode(response.headers.get_content_charset())
        i = str(html_content).index("list=") + 5
        search_results='https://www.youtube.com/playlist?list='
        while html_content[i]!='\"':
            search_results+=html_content[i]
            i=i+1

    #    self.infoLabel.set_text(search_results)
        return search_results

    def _playPlaylist(self, playlist) :

        self.playlistNames = []

        firstVideo = playlist['items'][0]['pafy']
        self._openVLCShell(firstVideo)

        self.playlistNames += [firstVideo.title]

        self.playlistThread = threading.Thread(target=self._addPlaylistItemsToVLCShell, args=[playlist])
        self.playlistThread.start()

    def _addPlaylistItemsToVLCShell(self, playlist) :
        for i in range(1, len(playlist['items'])) :
            print('adding '+playlist['items'][i]['pafy'].title)
            self.playlistNames += [playlist['items'][i]['pafy'].title]
            if self.AUDIO_ONLY :
                try :
                    self.vlcShell.stdin.write(bytes('enqueue '+playlist['items'][i]['pafy'].getbestaudio().url+'\n', 'utf-8'))
                except OSError :
                    continue
            else :
                try :
                    self.vlcShell.stdin.write(bytes('enqueue '+playlist['items'][i]['pafy'].getbest().url+'\n', 'utf-8'))
                except OSError :
                    continue

    def _showHelp(self, widget) :
        window = helpwindow.helpWindow()
        window.connect("delete-event", Gtk.main_quit)
        window.show_all()
        Gtk.main()
        return

    def _quitVLC(self, widget) :
        try :
            self.vlcShell.stdin.write(bytes('q\n', 'utf-8'))
            self.vlcShell.stdin.flush()

        except AttributeError :
            self.infoLabel.set_text("VLC is not running.")
        except BrokenPipeError :
            img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-start-symbolic"), Gtk.IconSize.BUTTON)
            self.playButton.set_image(img)
            self.vlcShell = None

    def _openVLCShell(self, video) :
        self.infoLabel.set_text(video.title)
        if self.AUDIO_ONLY == True :
            try :
                video_url = video.getbestaudio().url
            except OSError:
                self.infoLabel.set_text("Can't play the requested video")
            self.vlcShell = subprocess.Popen('cvlc --no-video --network-caching 10000 --extraintf rc'.split()+[video_url], stdin = subprocess.PIPE, stdout= subprocess.PIPE)

        else :
            try :
                video_url = video.getbest().url
            except OSError:
                self.infoLabel.set_text("Can't play the requested video")
            if MINIMAL_INTERFACE :
                self.vlcShell = subprocess.Popen('vlc --no-video-title --qt-minimal-view --extraintf rc'.split()+[video_url], stdin = subprocess.PIPE, stdout= subprocess.PIPE)
            else :
                self.vlcShell = subprocess.Popen('vlc --no-video-title --extraintf rc'.split()+[video_url], stdin = subprocess.PIPE, stdout= subprocess.PIPE)


    def _mininalInterface(self, widget) :
        self.MINIMAL_INTERFACE = widget.get_active()
