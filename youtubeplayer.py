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

oldURL = None

class YouTubePlayer(Gtk.Window) :
    def __init__(self) :

        self.AUDIO_ONLY = False
        self.MINIMAL_INTERFACE = True
        self.vlcShell = None
        self.downloadThread = None
        self.playlistThread = None
        self.playlistNames = []
        self.vidNo = 0
        self.clickCounter = 0


        Gtk.Window.__init__(self)
        self.set_border_width(10)
        self.set_size_request(500, 100)

        #Title bar tweaks
        headerBar = Gtk.HeaderBar()
        headerBar.set_show_close_button(True)
        headerBar.props.title = None
        self.set_titlebar(headerBar)
        self.set_resizable(False)
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

        adj = Gtk.Adjustment(0.0, 0.0, 100.0, 1.0, 10.0, 10.0)

        self.currentTime = Gtk.Label("0:00")
        self.totalTime = Gtk.Label("0:00")

        self.seekBar = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, adj)
        self.seekBar.set_hexpand(True)
        self.seekBar.set_draw_value(False)
        self.seekBar.set_property("width-request", 150)
        self.seekBar.set_digits(1)
        self.seekBar.set_value(100)

        headerBar.pack_start(self.buttonBox)
        headerBar.set_has_subtitle(False)
        headerBar.set_custom_title(self.seekBar)
        headerBar.set_decoration_layout('menu:close')
        headerBar.pack_start(self.currentTime)

    #    seekBox.pack_start(self.seekBar, True, True, 0)
        headerBar.pack_end(self.totalTime)

        self.seekThread = threading.Thread(target=self._setSeekBar)
        self.seekThread.setDaemon(True)
        self.seekThread.start()



        #############################################################

    def show(self) :
        self.show_all()
        self.seekBar.hide()
        self.currentTime.hide()
        self.totalTime.hide()

    def play(self, widget) :
        url = self.entry.get_text()
        global oldURL
        if (oldURL == url or url == '') and self.vlcShell != None:
            self.clickCounter += 1

            if url != '' :
                oldURL = url

            if self.clickCounter%2 == 0 :
                img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-start-symbolic"), Gtk.IconSize.BUTTON)
                self.vlcShell.stdin.write(bytes('pause\n', 'utf-8'))
                self.playButton.set_image(img)

            else :
                img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-pause-symbolic"), Gtk.IconSize.BUTTON)
                self.vlcShell.stdin.write(bytes('pause\n', 'utf-8'))
                self.playButton.set_image(img)

            try :
                self.vlcShell.stdin.flush()
                return
            except BrokenPipeError :
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

        if url == '' :
            self.infoLabel.set_text("I can't download nothing. XD")
            return

        if url[0] == '/' : # search term
            if url[1] == '/' :
                # Search for playlist
                self.infoLabel.set_text("Searching for playlist")
                url = self._getFirstYTResultURL_PL(url[2:])
            else :
                #Search for video
                self.infoLabel.set_text("Searching for video")
                url = self._getFirstYTResultURL(url[1:])


        if 'list=' not in url:
            video = pafy.new(url)


            if self.AUDIO_ONLY == True :
                self.downloadThread = threading.Thread(target=self._downloadAudio, args=[video])
                self.downloadThread.setDaemon(True)
                self.downloadThread.start()

            else:
                self.downloadThread = threading.Thread(target=self._download, args=[video])
                self.downloadThread.setDaemon(True)
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
            video.getbestaudio(preftype="m4a").download(filepath=os.environ.get('HOME')+'/Downloads/YouTubePlayer/'+video.title+'[audio].'+video.getbestaudio().extension, quiet=False, callback=self._setdownloadETA)
        except FileNotFoundError :
            os.makedirs(os.environ.get('HOME')+'/Downloads/YouTubePlayer')
            video.getbestaudio(preftype="m4a").download(filepath=os.environ.get('HOME')+'/Downloads/YouTubePlayer/'+video.title+'[audio].'+video.getbestaudio().extension, quiet=False, callback=self._setdownloadETA)

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
        self.playlistThread.setDaemon(True)
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
            self.vlcShell = subprocess.Popen('cvlc --no-video --network-caching 10000 --extraintf rc --meta-title '.split()+['"'+video.title+'"']+[video_url], stdin = subprocess.PIPE, stdout= subprocess.PIPE)

        else :
            try :
                video_url = video.getbest().url
            except OSError:
                self.infoLabel.set_text("Can't play the requested video")
            if self.MINIMAL_INTERFACE :
                self.vlcShell = subprocess.Popen('vlc --no-video-title --qt-minimal-view --extraintf rc --meta-title'.split()+['"'+video.title+'"']+[video_url], stdin = subprocess.PIPE, stdout= subprocess.PIPE)
            else :
                self.vlcShell = subprocess.Popen('vlc --no-video-title --extraintf rc'.split()+[video_url], stdin = subprocess.PIPE, stdout= subprocess.PIPE)


        self.currentTime.show()
        self.seekBar.show()
        self.totalTime.show()

    def _mininalInterface(self, widget) :
        self.MINIMAL_INTERFACE = widget.get_active()

    def _setSeekBar(self) :
        while True :
            sleep(1)

            try :
                self.vlcShell.stdout.flush()
                self.vlcShell.stdin.write(bytes('get_length\n', 'utf-8'))
                self.vlcShell.stdin.flush()
                c=0
                totalTime=0
                x = self.vlcShell.stdout.readline()
                try :
                    totalTime = int(str(x, 'utf-8')[2:-2])
                except ValueError :
                    continue
                if totalTime == 0 :
                    totalTime = 1
                self.totalTime.set_text(self._secondsToTime(totalTime))

                self.vlcShell.stdin.write(bytes('get_time\n', 'utf-8'))
                self.vlcShell.stdin.flush()
                x = self.vlcShell.stdout.readline()
                try :
                    currentTime = int(str(x, 'utf-8')[2:-2])
                except ValueError :
                    continue
                self.currentTime.set_text(self._secondsToTime(currentTime))

                self.seekBar.set_value(int((float(currentTime)/totalTime)*100))

            except BrokenPipeError :
                continue

            except AttributeError :
                continue

    def _secondsToTime(self, seconds) :
        t = ''
        t += str(int(seconds/60))
        t += ':'
        if seconds%60 <10:
            t+='0'+str(seconds%60)

        else :
            t += str(seconds%60)
        return t
