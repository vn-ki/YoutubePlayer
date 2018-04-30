from pydbus import SessionBus
from pydbus.generic import signal
from gi.repository import GLib

# TODO : Implement the seeked signal and seek through mpris


class MPRIS(object):
    def Raise(self):
        self.player.set_keep_above(True)
        self.player.set_keep_above(False)
        self.player.present()
        return

    def Quit(self):
        return

    def Next(self):
        self.player.next(None)

    def Previous(self):
        self.player.previous(None)

    def Pause(self):
        print("pause")

    def PlayPause(self):
        self.player.play(None)

    def Stop(self):
        print("stop")

    def Play(self):
        self.player.play()
        print('play')

    def Seek(self, o):
        # self.player._seek(o/1000)
        pass

    def SetPosition(self, TrackId, Position):
        self.Position = Position
        self.player._seek(Position // 1000)

    def OpenUri(self, s):
        print(s)

    def __init__(self):
        self._CanQuit = False
        self._CanRaise = True
        self._HasTrackList = False
        self._Identity = "YouTube Player"
        self._SupportedUriSchemes = ('file', 'http')
        self._SupportedMimeTypes = ('audio/mpeg')
        self._Metadata = None
        self._PlaybackStatus = "Stopped"
        self._Rate = 1.0
        self._Volume = 100
        self._Position = 1
        self._MinimumRate = 1.0
        self._MaximumRate = 1.0
        self._CanGoNext = True
        self._CanGoPrevious = True
        self._CanPlay = True
        self._CanPause = True
        self._CanSeek = True
        self._CanControl = True

    @property
    def CanQuit(self):
        return self._CanQuit

    @CanQuit.setter
    def CanQuit(self, value):
        self._CanQuit = value
        self.PropertiesChanged("org.mpris.MediaPlayer2",
                               {"CanQuit": self.CanQuit}, [])

    @property
    def CanRaise(self):
        return self._CanRaise

    @CanRaise.setter
    def CanRaise(self, value):
        self._CanRaise = value
        self.PropertiesChanged("org.mpris.MediaPlayer2",
                               {"CanRaise": self.CanRaise}, [])

    @property
    def HasTrackList(self):
        return self._HasTrackList

    @HasTrackList.setter
    def HasTrackList(self, value):
        self._HasTrackList = value
        self.PropertiesChanged("org.mpris.MediaPlayer2",
                               {"HasTrackList": self.HasTrackList}, [])

    @property
    def Identity(self):
        return self._Identity

    @Identity.setter
    def Identity(self, value):
        self._Identity = value
        self.PropertiesChanged("org.mpris.MediaPlayer2",
                               {"Identity": self.Identity}, [])

    @property
    def SupportedUriSchemes(self):
        return self._SupportedUriSchemes

    @SupportedUriSchemes.setter
    def SupportedUriSchemes(self, value):
        self._SupportedUriSchemes = value
        self.PropertiesChanged(
            "org.mpris.MediaPlayer2",
            {"SupportedUriSchemes": self.SupportedUriSchemes}, [])

    @property
    def SupportedMimeTypes(self):
        return self._SupportedMimeTypes

    @SupportedMimeTypes.setter
    def SupportedMimeTypes(self, value):
        self._SupportedMimeTypes = value
        self.PropertiesChanged("org.mpris.MediaPlayer2",
                               {"SupportedMimeTypes": self.SupportedMimeTypes},
                               [])

    ###

    @property
    def PlaybackStatus(self):
        return self._PlaybackStatus

    @PlaybackStatus.setter
    def PlaybackStatus(self, value):
        self._PlaybackStatus = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"PlaybackStatus": self.PlaybackStatus}, [])

    @property
    def Rate(self):
        return self._Rate

    @Rate.setter
    def Rate(self, value):
        self._Rate = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"Rate": self.Rate}, [])

    @property
    def Metadata(self):
        return self._Metadata

    @Metadata.setter
    def Metadata(self, value):
        self._Metadata = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"Metadata": self.Metadata}, [])

    @property
    def Volume(self):
        return self._Volume

    @Volume.setter
    def Volume(self, value):
        self._Volume = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"Volume": self.Volume}, [])

    @property
    def Position(self):
        return self._Position

    @Position.setter
    def Position(self, value):
        self._Position = value

    @property
    def MinimumRate(self):
        return self._MinimumRate

    @MinimumRate.setter
    def MinimumRate(self, value):
        self._MinimumRate = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"MinimumRate": self.MinimumRate}, [])

    @property
    def MaximumRate(self):
        return self._MaximumRate

    @MaximumRate.setter
    def MaximumRate(self, value):
        self._MaximumRate = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"MaximumRate": self.MaximumRate}, [])

    @property
    def CanGoNext(self):
        return self._CanGoNext

    @CanGoNext.setter
    def CanGoNext(self, value):
        self._CanGoNext = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"CanGoNext": self.CanGoNext}, [])

    @property
    def CanGoPrevious(self):
        return self._CanGoPrevious

    @CanGoPrevious.setter
    def CanGoPrevious(self, value):
        self._CanGoPrevious = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"CanGoPrevious": self.CanGoPrevious}, [])

    @property
    def CanPlay(self):
        return self._CanPlay

    @CanPlay.setter
    def CanPlay(self, value):
        self._CanPlay = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"CanPlay": self.CanPlay}, [])

    @property
    def CanPause(self):
        return self._CanPause

    @CanPause.setter
    def CanPause(self, value):
        self._CanPause = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"CanPause": self.CanPause}, [])

    @property
    def CanSeek(self):
        return self._CanSeek

    @CanSeek.setter
    def CanSeek(self, value):
        self._CanSeek = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"CanSeek": self.CanSeek}, [])

    @property
    def CanControl(self):
        return self._CanControl

    @CanControl.setter
    def CanControl(self, value):
        self._CanControl = value
        self.PropertiesChanged("org.mpris.MediaPlayer2.Player",
                               {"CanControl": self.CanControl}, [])

    PropertiesChanged = signal()
    Seeked = signal()
