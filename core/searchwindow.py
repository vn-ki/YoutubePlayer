import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import pafy
import urllib
import json

PAFY_OBJECT = None

def _getYTResultURL(query, result=0)  :
    key = 'AIzaSyDvysm00R5FClmqtxcATsgpKHdt2GxCaiU'

    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&'
    t = urllib.parse.urlencode({"q" : query})
    url += t + '&'
    t = urllib.parse.urlencode({"key" : key})
    url += t

    try :
        response = urllib.request.urlopen(url)

    except urllib.error.URLError :
        return -1
    data = json.loads(response.read())

    search_results = []

    for x in data['items'] :
        d = dict()
        d['id'] = x['id']['videoId']
        d['title'] = x['snippet']['title']
        search_results.append(d)

    return search_results

def _getYTResultURL_PL(query, result=0) :
    query_string = urllib.parse.urlencode({"search_query" :  'playlist ' + query})
    try :
        response = urllib.request.urlopen("https://www.youtube.com/results?" + query_string + "&sp=EgIQAw%253D%253D")
    except urllib.error.URLError :
        return -1
    html_content=response.read().decode(response.headers.get_content_charset())
    i = str(html_content).index("list=") + 5
    search_results='https://www.youtube.com/playlist?list='
    while html_content[i]!='\"':
        search_results+=html_content[i]
        i=i+1

    return search_results

class SearchBox(Gtk.Box) :
    def __init__(self, vidTitle, id) :
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=0)
        title = Gtk.Label()
        title.set_line_wrap(True)
        title.set_size_request(300,-1)
        title.set_xalign(0.01)

        self.pack_start(title, True, True, 0)
        self.set_size_request(300, -1)

        toolbar = Gtk.Toolbar()
        toolbar.set_icon_size(Gtk.IconSize.BUTTON)

        self.pack_start(toolbar, True,True,0)


        self.playButton = Gtk.ToolButton()
        self.playButton.connect('clicked', self.playButtonClicked)
        self.playButton.set_icon_name('media-playback-start-symbolic')
        toolbar.insert(self.playButton, -1)

        self.downloadButton = Gtk.ToolButton()
        self.downloadButton.connect('clicked', self.downloadButtonClicked)
        self.downloadButton.set_icon_name('folder-download-symbolic')
        toolbar.insert(self.downloadButton, -2)

        title.set_text(vidTitle)

    def playButtonClicked(self, widget) :
        pass

    def downloadButtonClicked(self, widget) :
        pass

class SearchWindow(Gtk.Window) :
    def __init__(self) :
        Gtk.Window.__init__(self, title='Search')

        self.set_border_width(10)
        self.set_size_request(400, 300)
        #self.set_resizable(False)

    def populate_box(self, searchterm) :
        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing =4)
        self.add(mainBox)

        if searchterm[0] == '/' :
            if searchterm[1] == '/' :
                fun = _getYTResultURL_PL
                query = searchterm[2:]
            else :
                fun = _getYTResultURL
                query = searchterm[1:]
        boxes =[]
        frames= []
        result = fun(query)
        i=0
        print(result)
        for x in result :
            if result == -1 :
                print("Error")
                continue
            boxes += [SearchBox(x['title'], x['id'])]
            frames += [Gtk.Frame()]
            frames[i].add(boxes[i])
            frames[i].set_size_request(300,-1)
            mainBox.pack_start(frames[i], True, True, 0)
            i+=1
