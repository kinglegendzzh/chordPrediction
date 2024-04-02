<h2>ChordPrediction</h2>
<a href='https://github.com/kinglegendzzh/chordPrediction/blob/master/README_EN.md'>English</a> <a href='https://github.com/kinglegendzzh/chordPrediction/blob/master/README.md'>中文</a>
<blockquote>

<p>Intelligent Music Composition Tool (Based on Markov Chain Chord Prediction Algorithm)</p>

<p>Chord prediction is one of the significant applications in the music generation field. This system proposes a chord prediction algorithm based on n-th order Markov chains, applied to real-time chord prediction. The algorithm first constructs a Markov chain based on historical chord sequences, then generates the next chord based on the current state of the chord sequence. When trained with multiple chord sequences, this algorithm can better handle transitions between different musical styles, thereby enhancing the diversity of the generated results.</p>

<p>The system also offers an interactive interface for applying this algorithm. Users can generate the chords they need through simple playing, as well as annotate, save, and preview chords, and independently train the model's accuracy. After performance evaluation, the algorithm, based on model data, can predict high-quality chords while ensuring prediction speed and stability.</p>
</blockquote>

ChordPrediction is an advanced tool designed for the purpose of intelligent music composition, leveraging a chord prediction algorithm based on Markov chains. This innovative system introduces a method for real-time chord prediction, which constructs a Markov chain from historical chord sequences and uses the current chord sequence state to generate the next chord. The algorithm is trained on multiple chord sequences to better handle transitions between different musical styles, thereby enhancing the diversity of the generated results.

The system also features an interactive interface that allows users to generate desired chords through simple playing. It enables users to annotate, save, and preview chords, and even train the model for accuracy. Through performance evaluation, the algorithm has demonstrated the capability to predict high-quality chords while ensuring prediction speed and stability.

<h3>System Overview</h3>
<img width="726" alt="DraggedImage" src="https://github.com/kinglegendzzh/chordPrediction/assets/33552269/9f731d4e-9f4b-4282-ae57-2c272437475f">
<h3>Interface Elements:</h3>

1. Current Chord
2. Predict the next chord and its match degree
3. Real-time chord sequence recording
4. Selected algorithm accuracy
5. Selected musical style/label
6. Save the current chord sequence to history
7. Annotate the current chord sequence to model data
8. Preview of historical records
9. Preview of model annotations
10. Real-time listening virtual mapping MIDI keyboard

<h3>Currently Supported MIDI Devices:</h3>

Professional MIDI keyboards with 49 keys or more (Best compatible brand: Icon iKeyBoard5 49 keys)
<h3>Background in Music Composition</h3>
Chords, being the core element of music composition akin to the foundation of a house, play a critical role in setting the style, ambiance, and emotional tone of a piece. This tool aims to support the chord design phase of music production by automating chord prediction and generation, thus facilitating more innovative and creative musical works.

<h3>How This System Aids in Music Composition</h3>
By analyzing existing chord combinations and model data, ChordPrediction can automatically generate new chord predictions, assisting in creating more novel and creative musical pieces. This system shortens the composition time for producers, allowing for the integration of system-generated chords into their works for enhanced effects and quality. Without such a system, musicians might spend considerable time and effort manually analyzing chord progressions, whereas ChordPrediction offers a quick and automated way to generate new chord combinations.

<h3>Libraries and Installation</h3>
To use this system, ensure you have Python 3.9 or later, musicpy, PyQt5, and pygame installed. Details on installation and generating executable files are provided, including a method using pyinstaller and direct download from the GitHub releases page.

<h3>Future Updates and Author's Note</h3>
The README outlines potential future updates with varying priorities, reflecting the author's commitment to improving and expanding the system. The author shares their journey into music theory and composition, expressing gratitude towards the community and inviting feedback and suggestions to fuel further development.

For more information and updates, visit the <a herf='https://github.com/kinglegendzzh/chordPrediction'>GitHub repository</a>.
