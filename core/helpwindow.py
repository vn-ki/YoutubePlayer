import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class helpWindow(Gtk.Window) :
    def __init__(self) :
        Gtk.Window.__init__(self, title='Help')
        self.set_border_width(10)
        self.set_size_request(400, 400)

        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(mainBox)

        img = Gtk.Image.new_from_file('images/icons/youtube-icon.png')
        youtubeButton = Gtk.Button(name="youtube-button", image=img)
        youtubeButton.connect('clicked', self.buttonClicked)
        mainBox.pack_start(youtubeButton, True, True, 0)

        infoLabel = Gtk.Label()
        infoLabel.set_markup(
        '''
                    <big><b> YouTubePlayer </b></big>

                            <i> Contributors </i>
                       <i>Vishnunarayan K I </i>
                      <i>Tarun Kumar Singh </i>

                    <b> Usage Information </b>

<b>1.</b> If you have a youtube link in hand, paste it
          in the url tab and press play.

<b>2.</b> If you want to search for a specific video,
          type <i>/search_term</i> in the url bar.

<b>3.</b> If you want to search for a playlist, type
          <i>//search_term</i> in the url bar.

        '''
        )

        mainBox.pack_start(infoLabel, True, True, 0)

    def buttonClicked(self, widget) :
        return
