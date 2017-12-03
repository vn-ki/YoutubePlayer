#!/usr/bin/python3

import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import youtubeplayer

window = youtubeplayer.YouTubePlayer()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
