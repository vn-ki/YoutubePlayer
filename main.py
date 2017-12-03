import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window) :
    def __init__(self) :
        Gtk.Window.__init__(self, title="YouTube Player")
        self.set_border_width(10)

        ##
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        ##

        self.entry = Gtk.Entry()
        self.mainBox.pack_start(self.entry, True, True, 0)

        ##

        self.checkButtonBox = Gtk.Box(spacing=10)
        self.mainBox.pack_start(self.checkButtonBox, True, True, 0)
        self.audioOnlyButton = Gtk.CheckButton("Audio only")
        self.checkButtonBox.pack_start(self.audioOnlyButton, True, True,0)

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

    #    self.button4 = Gtk.Button(label='Button2')
    #    self.button4.connect('clicked', self.clickedFoo)
    #    self.buttonBox.pack_start(self.button4, True, True, 0)

    def previous(self, widget) :
        return
    def play(self, widget) :
        return
    def next(self, widget) :
        return


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
