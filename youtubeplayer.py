import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class YouTubePlayer(Gtk.Window) :
    def __init__(self) :

        self.AUDIO_ONLY = False
        self.vlcShell = None

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
                #pafy code goes here

                video_url = ''  # URL from pafy; for tarun


                if self.AUDIO_ONLY == true :
                    self.vlcShell = subprocess.Popen('cvlc --no-video --extraintf="rc" '.split()+video_url)
                else :
                    self.vlcShell = subprocess.Popen('vlc --qt-minimal-view --extraintf="rc" '.split()+video_url)

                return
            else : # A playlist
            #You'll most propably have to use threading module
            #while playing playlist
            #Try looking into that.
            #Else I can do it.
            #And use get_playlist2() and iterate through it
            #rather than using get_playlist()


                return

        #else do play pause using lib vlc
        if self.playButton.get_label() == 'Play' :
            self.vlcShell.stdin.write(bytes('play', 'utf-8'))
            self.vlcShell.stdin.flush()
            self.playButton.set_label('Pause')
        else :
            self.vlcShell.stdin.write(bytes('pause', 'utf-8'))
            self.vlcShell.stdin.flush()
            self.playButton.set_label('Play')
        return

    def next(self, widget) :
        self.vlcShell.stdin.write(bytes('next', 'utf-8'))
        self.vlcShell.stdin.flush()
        return

    def previous(self, widget) :
        self.vlcShell.stdin.write(bytes('prev', 'utf-8'))
        self.vlcShell.stdin.flush()
        return

    def download(self, widget) :
        #I'll do it, later.
        return

    def audioOnly(self, widget) :
        self.AUDIO_ONLY = widget.get_active()
        return
