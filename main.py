#!/usr/bin/python3

import gi
import subprocess
import threading

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import youtubeplayer

window = youtubeplayer.YouTubePlayer()
window.set_icon_from_file('images/icons/youtube.svg')
window.connect("delete-event", Gtk.main_quit)
window.connect('key-release-event', window.keyPressed)
window.show()

Gtk.main()
