ChordPrediction

ChordPrediction is an advanced tool designed for the purpose of intelligent music composition, leveraging a chord prediction algorithm based on Markov chains. This innovative system introduces a method for real-time chord prediction, which constructs a Markov chain from historical chord sequences and uses the current chord sequence state to generate the next chord. The algorithm is trained on multiple chord sequences to better handle transitions between different musical styles, thereby enhancing the diversity of the generated results.

The system also features an interactive interface that allows users to generate desired chords through simple playing. It enables users to annotate, save, and preview chords, and even train the model for accuracy. Through performance evaluation, the algorithm has demonstrated the capability to predict high-quality chords while ensuring prediction speed and stability.

System Overview
System Preview

Interface Elements:

Current Chord
Predict the next chord and its match degree
Real-time chord sequence recording
Selected algorithm accuracy
Selected musical style/label
Save the current chord sequence to history
Annotate the current chord sequence to model data
Preview of historical records
Preview of model annotations
Real-time listening virtual mapping MIDI keyboard
Currently Supported MIDI Devices:

Professional MIDI keyboards with 49 keys or more (Best compatible brand: Icon iKeyBoard5 49 keys)
Background in Music Composition
Chords, being the core element of music composition akin to the foundation of a house, play a critical role in setting the style, ambiance, and emotional tone of a piece. This tool aims to support the chord design phase of music production by automating chord prediction and generation, thus facilitating more innovative and creative musical works.

How This System Aids in Music Composition
By analyzing existing chord combinations and model data, ChordPrediction can automatically generate new chord predictions, assisting in creating more novel and creative musical pieces. This system shortens the composition time for producers, allowing for the integration of system-generated chords into their works for enhanced effects and quality. Without such a system, musicians might spend considerable time and effort manually analyzing chord progressions, whereas ChordPrediction offers a quick and automated way to generate new chord combinations.

Libraries and Installation
To use this system, ensure you have Python 3.9 or later, musicpy, PyQt5, and pygame installed. Details on installation and generating executable files are provided, including a method using pyinstaller and direct download from the GitHub releases page.

Future Updates and Author's Note
The README outlines potential future updates with varying priorities, reflecting the author's commitment to improving and expanding the system. The author shares their journey into music theory and composition, expressing gratitude towards the community and inviting feedback and suggestions to fuel further development.

For more information and updates, visit the GitHub repository.