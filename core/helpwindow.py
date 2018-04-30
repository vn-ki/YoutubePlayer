import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

from core import util


class helpWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Settings')
        self.set_border_width(10)
        # self.set_size_request(400, 400)

        notebook = Gtk.Notebook()

        self.add(notebook)

        settingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        settingLabel = Gtk.Label("Settings")
        notebook.append_page(settingBox, settingLabel)
        self.data = util.readFromConfig()

        smallBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        settingBox.pack_start(smallBox, True, True, 0)
        self.audioOnlyButton = Gtk.CheckButton("Default show video")
        self.audioOnlyButton.connect('toggled', self.audioOnly)
        self.audioOnlyButton.set_focus_on_click(False)
        smallBox.pack_start(self.audioOnlyButton, True, True, 0)

        okButtonBox = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        settingBox.pack_end(okButtonBox, True, True, 0)
        cancelButton = Gtk.Button("Cancel")
        okButtonBox.pack_end(cancelButton, True, True, 0)

        okButton = Gtk.Button("Save")
        okButtonBox.pack_end(okButton, True, True, 0)
        okButton.connect('clicked', self.save)

        aboutBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        aboutLabel = Gtk.Label("About")
        notebook.append_page(aboutBox, aboutLabel)

        OPTIONS = ['Low', 'Medium', 'High']
        keys = {'Low': 0, 'Medium': 1, 'High': 2}

        comboBox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        smallBox.pack_start(comboBox1, True, True, 0)
        vidQualityLabel = Gtk.Label("Video Quality : ")
        comboBox1.pack_start(vidQualityLabel, True, True, 0)
        vidQuality = Gtk.ComboBoxText()
        vidQuality.set_entry_text_column(0)
        vidQuality.connect('changed', self.vidQualityChanged)
        for option in OPTIONS:
            vidQuality.append_text(option)
        vidQuality.set_active(keys[self.data['VID_QUALITY']])
        comboBox1.pack_start(vidQuality, True, True, 0)

        comboBox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        smallBox.pack_start(comboBox2, True, True, 0)
        audQuality = Gtk.ComboBoxText()
        audQualityLabel = Gtk.Label("Video Quality : ")
        comboBox2.pack_start(audQualityLabel, True, True, 0)
        audQuality.set_entry_text_column(0)
        audQuality.connect('changed', self.audQualityChanged)
        for option in OPTIONS:
            audQuality.append_text(option)
        audQuality.set_active(keys[self.data['AUD_QUALITY']])
        comboBox2.pack_start(audQuality, True, True, 0)

        comboBox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        smallBox.pack_start(comboBox3, True, True, 0)
        dl_videoQuality = Gtk.ComboBoxText()
        dl_videoQualityLabel = Gtk.Label("Download Video Quality : ")
        comboBox3.pack_start(dl_videoQualityLabel, True, True, 0)
        dl_videoQuality.set_entry_text_column(0)
        dl_videoQuality.connect('changed', self.audQualityChanged)
        for option in OPTIONS:
            dl_videoQuality.append_text(option)
        dl_videoQuality.set_active(keys[self.data['DL_VID_QUALITY']])
        comboBox3.pack_start(dl_videoQuality, True, True, 0)

        comboBox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        smallBox.pack_start(comboBox4, True, True, 0)
        dl_audQuality = Gtk.ComboBoxText()
        dl_audQualityLabel = Gtk.Label("Download Audio Quality : ")
        comboBox4.pack_start(dl_audQualityLabel, True, True, 0)
        dl_audQuality.set_entry_text_column(0)
        dl_audQuality.connect('changed', self.dl_audQualityChanged)
        for option in OPTIONS:
            dl_audQuality.append_text(option)
        dl_audQuality.set_active(keys[self.data['DL_AUD_QUALITY']])
        comboBox4.pack_start(dl_audQuality, True, True, 0)

        img = Gtk.Image.new_from_file('images/icons/youtube-icon.png')
        youtubeButton = Gtk.Button(name="youtube-button", image=img)
        youtubeButton.connect('clicked', self.buttonClicked)
        aboutBox.pack_start(youtubeButton, True, True, 0)

        infoLabel = Gtk.Label()
        infoLabel.set_markup('''
                <i> Contributors </i>
           <i>Vishnunarayan K I </i>
          <i>Tarun Kumar Singh </i>
        ''')

        aboutBox.pack_start(infoLabel, True, True, 0)

    def buttonClicked(self, widget, d=None):
        self.hide()
        return

    def show_function(self):
        self.show_all()
        self.data = util.readFromConfig()

    def audioOnly(self, w):
        self.data['AUDIO_ONLY'] = w.get_active()

    def vidQualityChanged(self, widget):
        text = widget.get_active_text()
        self.data['VID_QUALITY'] = text

    def audQualityChanged(self, widget):
        text = widget.get_active_text()
        self.data['AUD_QUALITY'] = text

    def dl_videoQualityChanged(self, widget):
        text = widget.get_active_text()
        self.data['VID_QUALITY'] = text

    def dl_audQualityChanged(self, widget):
        text = widget.get_active_text()
        self.data['AUD_QUALITY'] = text

    def save(self, w):
        util.writeToConfig(self.data)
        self.buttonClicked(None)

    def cancel(self, w):
        self.buttonClicked(None)
