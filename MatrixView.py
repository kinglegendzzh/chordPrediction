import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from service.numpyMarkov import ChordPredictor
import io


class MatrixView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("概率转移矩阵的和弦分布图")
        self.setGeometry(200, 200, 500, 400)

        # Initialize variables
        self.chord_sequences = []
        self.needs_update = False  # Flag to control image updates

        # Set up the label to display the image
        self.label = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

        # Since QMainWindow cannot have a layout directly, set a central widget
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def set_chord_sequences(self, chord_sequences):
        """Set new chord sequences and update the image if they have changed."""
        if chord_sequences != self.chord_sequences:
            self.chord_sequences = chord_sequences
            self.needs_update = True
            self.update_image()

    def update_image(self):
        """Update the displayed image based on the current chord sequences."""
        if not self.needs_update or not self.chord_sequences:
            return
        # Create a matplotlib figure
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        # Create the predictor and plot the transition matrix
        self.predictor = ChordPredictor(self.chord_sequences, order=1)
        cax = ax.imshow(self.predictor.transitions, cmap='hot', interpolation='nearest')
        fig.colorbar(cax)
        ax.set_title("Transition Matrix Heatmap")
        ax.set_xlabel("Next Chord Index")
        ax.set_ylabel("Current State Index")
        # Render the figure to a buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        # Load the image from the buffer and set it to the label
        img = QImage.fromData(buf.getvalue())
        pixmap = QPixmap.fromImage(img)
        self.label.setPixmap(pixmap)
        buf.close()
        self.update()
        self.needs_update = False
