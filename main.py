import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class MainWindow(Gtk.Window) :
    def __init__(self) :
        self.AUDIO_ONLY = False

        Gtk.Window.__init__(self, title="YouTube Player")
        self.set_border_width(10)
        self.set_size_request(400, 100)


        ## Main Box: All widgets are inside this
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        ##

        #Input box
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("URL")
        self.mainBox.pack_start(self.entry, True, True, 0)

        ##

        self.checkButtonBox = Gtk.Box(spacing=10)
        self.mainBox.pack_start(self.checkButtonBox, True, True, 0)
        self.audioOnlyButton = Gtk.CheckButton("Audio only")
        self.audioOnlyButton.connect('toggled', self.audioOnly)
        self.checkButtonBox.pack_start(self.audioOnlyButton, True, True,0)

        self.downloadButton = Gtk.Button(label='Download')
        self.downloadButton.connect('clicked', self.download)
        self.checkButtonBox.pack_start(self.downloadButton, True,True,0)
        ##
        self.buttonBox = Gtk.Box(spacing=10)
        self.mainBox.pack_start(self.buttonBox, True,True, 0)
        self.add(self.mainBox)

        self.prevButton = Gtk.Button(label='Prev')
        self.prevButton.connect('clicked', self.previous)
        self.buttonBox.pack_start(self.prevButton, True, True, 0)

        self.playButton = Gtk.Button(label='Play')
        self.playButton.connect('clicked', self.play)
        self.buttonBox.pack_start(self.playButton, True, True, 0)

        self.nextButton = Gtk.Button(label='Next')
        self.nextButton.connect('clicked', self.next)
        self.buttonBox.pack_start(self.nextButton, True, True, 0)


    def play(self, widget) :
        url = self.entry.get_text()
        if url!='' :
            #Use pafy

            video_url = ''  # URL from pafy; for tarun


            if self.AUDIO_ONLY == true :
                subprocess.Popen('cvlc --no-video '.split()+video_url)
            else :
                subprocess.Popen('vlc --qt-minimal-view '.split()+video_url)

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
        #preferably using youtube-dl
        return

    def audioOnly(self, widget) :
        self.AUDIO_ONLY = widget.get_active()
        return


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
