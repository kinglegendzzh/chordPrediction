import numpy as np


class ChordPredictor:
    def __init__(self, chord_sequences, order=1):
        self.order = order
        self.chord_index = self.index_chords(chord_sequences)
        self.n_chords = len(self.chord_index)
        self.transitions = np.zeros((self.n_chords ** self.order, self.n_chords))

        self.build_transition_matrix(chord_sequences)

    def index_chords(self, sequences):
        unique_chords = set()
        for seq in sequences:
            unique_chords.update(seq)
        return {chord: i for i, chord in enumerate(unique_chords)}

    def build_transition_matrix(self, sequences):
        for seq in sequences:
            for i in range(len(seq) - self.order):
                cur_state = tuple(seq[i:i + self.order])
                cur_state_index = self.state_to_index(cur_state)
                next_chord_index = self.chord_index[seq[i + self.order]]
                self.transitions[cur_state_index, next_chord_index] += 1

        for i in range(len(self.transitions)):
            row_sum = np.sum(self.transitions[i])
            if row_sum > 0:
                self.transitions[i] /= row_sum

    def state_to_index(self, state):
        index = 0
        for j, chord in enumerate(state):
            index += self.chord_index[chord] * (self.n_chords ** (self.order - j - 1))
        return index

    def predict_chord(self, current_chords, threshold=0.1):
        if len(current_chords) < self.order:
            raise ValueError("The number of current chords is less than the order of the Markov Chain.")

        cur_state = tuple(current_chords[-self.order:])
        cur_state_index = self.state_to_index(cur_state)
        probabilities = self.transitions[cur_state_index]
        next_chords = [(list(self.chord_index.keys())[i], prob) for i, prob in enumerate(probabilities) if
                       prob > threshold]

        # Sort by probability in descending order and normalize probabilities
        next_chords = sorted(next_chords, key=lambda x: x[1], reverse=True)
        total_prob = sum(prob for _, prob in next_chords)
        next_chords = [(chord, prob / total_prob) for chord, prob in next_chords]

        return next_chords


if __name__ == '__main__':
    chord_sequences = [
        ['C', 'Am', 'F', 'G', 'C'],
        ['Am', 'F', 'C', 'G', 'Am']
    ]
    predictor = ChordPredictor(chord_sequences, order=1)
    current_chords = ['C']
    next_chords = predictor.predict_chord(current_chords, threshold=0.1)
    print('Predictions:')
    for chord, prob in next_chords:
        print(f"{chord}: {prob:.2f}")
