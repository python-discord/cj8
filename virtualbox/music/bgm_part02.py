# part02

from earsketch import *

init()
setTempo(120)

fitMedia(RD_EDM_CHORDPART_7, 1, 1, 9)
fitMedia(RD_EDM_CHORDPART_2, 2, 1, 9)
fitMedia(RD_EDM_CHORDPART_4, 3, 1, 9)
fitMedia(RD_EDM_CHORDPART_6, 4, 1, 9)
fitMedia(RD_EDM_CHORDPART_1, 5, 1, 9)
fitMedia(RD_EDM_CHORDPART_5, 6, 1, 9)
fitMedia(RD_EDM_CHORDPART_8, 7, 1, 9)
fitMedia(RD_EDM_MAINBEAT_2, 8, 1, 9)
fitMedia(RD_EDM_MAINBEAT_18, 9, 2, 3)
fitMedia(RD_EDM_MAINBEAT_18, 9, 7, 8)
fitMedia(RD_EDM_MAINBEAT_15, 10, 1, 9)
fitMedia(YG_HIP_HOP_PIANO_2, 11, 1, 2)
fitMedia(YG_HIP_HOP_PIANO_2, 11, 5, 7)
fitMedia(HOUSE_DEEP_DREAMPAD_002, 12, 1, 2.5)
fitMedia(HOUSE_SFX_WHOOSH_001, 13, 8, 9)

setEffect(12,VOLUME,GAIN,10,1,10,9)
setEffect(13,VOLUME,GAIN,0,1,0,9)
setEffect(11,VOLUME,GAIN,5,1,5,9)
setEffect(MIX_TRACK,VOLUME,GAIN,-25,1,-25,9)

finish()
