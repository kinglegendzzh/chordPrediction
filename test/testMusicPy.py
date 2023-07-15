import musicpy
from musicpy.musicpy import get_chord, trans, N
from musicpy.structures import scale
import musicpy.algorithms

print(trans('Aminor/C'))
# p.modulation(scale('A', 'major'), scale('A', 'minor'))

str = musicpy.algorithms.detect([N('D#1'), N('C2')], get_chord_type=True)

print(str)
print(str.root)