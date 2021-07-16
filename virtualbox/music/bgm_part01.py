# part01

from earsketch import *
init()
setTempo(120)

fitMedia(RD_EDM_SFX_RISER_AIR_1, 1, 1, 5)
fitMedia(RD_EDM_SFX_RISER_AIR_2, 2, 1, 5)
fitMedia(RD_EDM_SFX_RISER_AIR_2, 2, 17, 21)
fitMedia(RD_EDM_CHORDPART_7, 3, 1, 21)
fitMedia(RD_EDM_CHORDPART_2, 4, 5, 21)
fitMedia(RD_EDM_CHORDPART_4, 5, 5, 21)
fitMedia(RD_EDM_CHORDPART_6, 6, 5, 21)
fitMedia(RD_EDM_CHORDPART_1, 7, 17, 21)
fitMedia(RD_EDM_CHORDPART_5, 8, 17, 21)
fitMedia(RD_EDM_CHORDPART_8, 9, 17, 21)
fitMedia(RD_EDM_MAINBEAT_2, 10, 5, 21)
fitMedia(YG_EDM_KICKS_2, 11, 1, 5)
fitMedia(RD_EDM_MAINBEAT_18, 11, 10, 11)
fitMedia(RD_EDM_MAINBEAT_18, 11, 15, 16)
fitMedia(HOUSE_DEEP_DREAMPAD_002, 12, 5, 6.5)
fitMedia(HOUSE_DEEP_DREAMPAD_002, 12, 13, 14.5)
fitMedia(HOUSE_SFX_WHOOSH_001, 13, 8.5, 10.5)
fitMedia(HOUSE_SFX_WHOOSH_001, 13, 18, 20)

setEffect(12,VOLUME,GAIN,10,9,10,21)
setEffect(13,VOLUME,GAIN,0,1,0,21)
setEffect(MIX_TRACK,VOLUME,GAIN,-60,1,-40,5)
setEffect(MIX_TRACK,VOLUME,GAIN,-45,5,-45,21)

finish()
