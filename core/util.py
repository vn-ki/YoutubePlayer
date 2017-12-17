import urllib, json
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

API_KEY = 'AIzaSyDvysm00R5FClmqtxcATsgpKHdt2GxCaiU'

def _getYTResultURL(query)  :
    url = 'https://www.googleapis.com/youtube/v3/search?type=video&part=snippet&'
    t = urllib.parse.urlencode({"q" : query})
    url += t + '&'
    t = urllib.parse.urlencode({"key" : API_KEY})
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

def _getYTResultURL_PL(query) :
    url = 'https://www.googleapis.com/youtube/v3/search?type=playlist&part=snippet&'
    t = urllib.parse.urlencode({"q" : query})
    url += t + '&'
    t = urllib.parse.urlencode({"key" : API_KEY})
    url += t

    try :
        response = urllib.request.urlopen(url)

    except urllib.error.URLError :
        return -1

    data = json.loads(response.read())
    search_results = []

    for x in data['items'] :
        d = dict()
        d['id'] = x['id']['playlistId']
        d['title'] = x['snippet']['title']
        search_results.append(d)

    return search_results

class SearchBox(Gtk.Frame) :
    def __init__(self, ytid='', title='') :
        Gtk.Frame.__init__(self)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.set_size_request(450,30)
        self.add(self.box)
        self.ytid = ytid

        self.title = Gtk.Label(title)
        self.title.set_xalign(0.01)
        self.title.set_line_wrap(True)
        #TODO
        self.img = ytid

        self.box.pack_start(self.title, True, True, 0)

    def setTitleAndId(self, title, ytid) :
        self.title.set_text(title)
        self.ytid = ytid
