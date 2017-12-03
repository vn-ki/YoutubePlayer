import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class YouTubePlayer(Gtk.Window) :
    def __init__(self) :
        self.AUDIO_ONLY = False

        Gtk.Window.__init__(self, title="YouTube Player")
        self.set_border_width(10)
        self.set_size_request(400, 100)

        ####################################################################
        ## Main Box: All widgets are inside this
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        ##

        #Input box
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("URL")
        self.mainBox.pack_start(self.entry, True, True, 0)


        #############################################################
        #Button for 2nd line, checkbox and download button
        #
        #Check box
        self.checkButtonBox = Gtk.Box(spacing=10)
        self.mainBox.pack_start(self.checkButtonBox, True, True, 0)
        self.audioOnlyButton = Gtk.CheckButton("Audio only")
        self.audioOnlyButton.connect('toggled', self.audioOnly)
        self.checkButtonBox.pack_start(self.audioOnlyButton, True, True,0)

        #Download button
        self.downloadButton = Gtk.Button(label='Download')
        self.downloadButton.connect('clicked', self.download)
        self.checkButtonBox.pack_start(self.downloadButton, True,True,0)
        #############################################################

        #############################################################
        #Box for lower buttons
        #

        self.buttonBox = Gtk.Box(spacing=10)
        self.mainBox.pack_start(self.buttonBox, True,True, 0)
        self.add(self.mainBox)

        #Previous button
        self.prevButton = Gtk.Button(label='Prev')
        self.prevButton.connect('clicked', self.previous)
        self.buttonBox.pack_start(self.prevButton, True, True, 0)

        #Play button
        self.playButton = Gtk.Button(label='Play')
        self.playButton.connect('clicked', self.play)
        self.buttonBox.pack_start(self.playButton, True, True, 0)

        #Next button
        self.nextButton = Gtk.Button(label='Next')
        self.nextButton.connect('clicked', self.next)
        self.buttonBox.pack_start(self.nextButton, True, True, 0)
        #############################################################

    def play(self, widget) :
        url = self.entry.get_text()
        if url!='' :
            #Use pafy
            if 'list' not in url : #Not a playist
                video_url = ''  # URL from pafy; for tarun


                if self.AUDIO_ONLY == true :
                    subprocess.Popen('cvlc --no-video '.split()+video_url)
                else :
                    subprocess.Popen('vlc --qt-minimal-view '.split()+video_url)

                return
            else : # A playlist

                return

        #else do play pause using lib vlc
        if self.playButton.get_label() == 'Play' :
            subprocess.run('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play'.split())
            self.playButton.set_label('Pause')
        else :
            subprocess.run('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause'.split())
            self.playButton.set_label('Play')
        return

    def next(self, widget) :
        subprocess.run('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next'.split())
        return

    def previous(self, widget) :
        subprocess.run('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous'.split())
        return

    def download(self, widget) :
        #For tarun
        #Research on how to download videos
        #Use pafy's download feature or YouTube-dl's downlaod feature
        #Youtube-dl would be more effitient
        return

    def audioOnly(self, widget) :
        self.AUDIO_ONLY = widget.get_active()
        return
