#!/usr/bin/python3

import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,
                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)

import youtubeplayer
from mpris import *
##
from pydbus import SessionBus
import pkg_resources



##

window = youtubeplayer.YouTubePlayer()
window.connect("delete-event", Gtk.main_quit)
window.show()
MPRIS.dbus = pkg_resources.resource_string(__name__, "mpris/mpris.xml").decode("utf-8")
MPRIS.pl = window
bus = SessionBus()
bus.publish('org.mpris.MediaPlayer2.YouTubePlayer', MPRIS(), ("/org/mpris/MediaPlayer2", MPRIS()))

Gtk.main()
