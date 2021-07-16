# part01

from earsketch import *
init()
setTempo(120)

fitMedia(RD_EDM_SFX_RISER_AIR_1, 1, 1, 5)
fitMedia(RD_EDM_SFX_RISER_AIR_2, 2, 1, 5)
fitMedia(RD_EDM_SFX_RISER_AIR_2, 2, 17, 21)
fitMedia(YG_EDM_KICKS_2, 11, 1, 5)
fitMedia(RD_EDM_CHORDPART_7, 3, 1, 21)
fitMedia(RD_EDM_CHORDPART_2, 4, 5, 21)
fitMedia(RD_EDM_CHORDPART_4, 5, 5, 21)
fitMedia(RD_EDM_CHORDPART_6, 6, 5, 21)
fitMedia(RD_EDM_CHORDPART_1, 7, 17, 21)
fitMedia(RD_EDM_CHORDPART_5, 8, 17, 21)
fitMedia(RD_EDM_CHORDPART_8, 9, 17, 21)
fitMedia(RD_EDM_MAINBEAT_2, 10, 5, 21)
fitMedia(RD_EDM_MAINBEAT_18, 11, 10, 11)
fitMedia(RD_EDM_MAINBEAT_18, 11, 15, 16)
setEffect(MIX_TRACK, VOLUME, GAIN, -60, 1, 0, 5)

finish()
