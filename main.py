from musicpy.musicpy import N, C, play
from musicpy.structures import note, chord

a = (C('Bmaj9',3)/[2,3,4,1,5]) % (1/8,1/8)
b = (C('Bmaj9',3)/[2,3,4,1,5,2]) % (1/8, 1/8)
q = a + ~a[1:-1]
q2 = b + ~b[3:-1]
t = (q + q2) * 2
adding = chord(['Bb5','Ab5','Gb5','Ab5']) % (1/2,1/2) * 2
t2 = t & adding
play(t2 + (t2 - 3), 100, instrument=47, wait=True)

# import musicpy as mp
#
# # 尼龙弦吉他分解和弦演奏一个和弦进行
#
# guitar = (C('CM7', 3, 1/4, 1/8)^2 |
#           C('G7sus', 2, 1/4, 1/8)^2 |
#           C('A7sus', 2, 1/4, 1/8)^2 |
#           C('Em7', 2, 1/4, 1/8)^2 |
#           C('FM7', 2, 1/4, 1/8)^2 |
#           C('CM7', 3, 1/4, 1/8)@1 |
#           C('AbM7', 2, 1/4, 1/8)^2 |
#           C('G7sus', 2, 1/4, 1/8)^2) * 2
#
# play(guitar, bpm=100, instrument=25, wait=True)