import gi
import subprocess
import pafy
import urllib

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def getplaylist(url):
    playlist=[]
    response = urllib.request.urlopen(url)
    html_content=response.read().decode(response.headers.get_content_charset())
    for i in range(len(html_content)):
        if html_content[i:i+6]=='watch?':
            playlist.append('https://www.youtube.com/watch?v='+html_content[i+8:i+19])
    return tuple(playlist)


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

        if self.vlcShell != None :
            if self.playButton.get_label() == 'Play' :
                self.vlcShell.stdin.write(bytes('play\n', 'utf-8'))
                self.playButton.set_label('Pause')
            else :
                self.vlcShell.stdin.write(bytes('pause\n', 'utf-8'))
                self.playButton.set_label('Play')
            try :
                self.vlcShell.stdin.flush()
                return
            except BrokenPipeError :
                self.vlcShell = None

        if url!='' :
            self.openVLC(url)


        #else do play pause using lib vlc

        return

    def openVLC(self,url) :
        if 'list=' not in url: #not a playlist

            ytvideo = False
            try: # check if given url is really a url or just a search term
                getyt=pafy.new(url)
                ytvideo=True
            except ValueError as e:
                print(e)
                ytvideo = False

            if ytvideo == True: #it is a video
                video_url = getyt.getbest().url
            else : # not a video
                query_string = urllib.parse.urlencode({"search_query" : url})
                response = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query_string)
                html_content=response.read().decode(response.headers.get_content_charset())
                i = str(html_content).index("watch?")
                search_results = html_content[i+8: i+19]
                video_url= pafy.new(search_results).getbest().url

            if self.AUDIO_ONLY == True :
                self.vlcShell = subprocess.Popen('cvlc --no-video --extraintf rc'.split()+[video_url], stdin = subprocess.PIPE)
            else :
                self.vlcShell = subprocess.Popen('vlc --no-video-title --qt-minimal-view --extraintf rc'.split()+[video_url], stdin = subprocess.PIPE)

        else: # A playlist
            videoindex = 0
            pl = []
            playlist = pafy.get_playlist2(url)
            for i in playlist:
                try:    # playlists often have links to those videos which do not exist
                    pl.append(i.getbest().url)
                except:
                    break
            video_url = pl[videoindex]
            #takes too long to load
            #will use threads
            if self.AUDIO_ONLY == True :
                self.vlcShell = subprocess.Popen('cvlc --no-video --extraintf rc'.split()+[video_url], stdin = subprocess.PIPE)
            else :
                self.vlcShell = subprocess.Popen('vlc --no-video-title --qt-minimal-view --extraintf rc'.split()+[video_url], stdin = subprocess.PIPE)
            return

    def next(self, widget) :
        self.vlcShell.stdin.write(bytes('next\n', 'utf-8'))
        self.vlcShell.stdin.flush()
        return

    def previous(self, widget) :
        self.vlcShell.stdin.write(bytes('prev\n', 'utf-8'))
        self.vlcShell.stdin.flush()
        return

    def download(self, widget) :
        return

    def audioOnly(self, widget) :
        self.AUDIO_ONLY = widget.get_active()
        return
