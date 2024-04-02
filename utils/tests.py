import unittest

from service.numpyMarkov import ChordPredictor


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    """
    测试ChordPredictor是否能够根据给定的和弦序列正确预测下一个和弦。
    """

    def test_basic_prediction(self):
        sequences = [['C', 'G', 'Am', 'F'], ['Am', 'F', 'C', 'G']]
        predictor = ChordPredictor(sequences, order=1)
        predictions = predictor.predict_chord(['G'])
        assert predictions, "预测失败，预测结果为空"
        print(f"基本功能测试通过,{predictions}")

    """
    测试在不同的order（阶数）设置下，ChordPredictor是否能够正常工作。
    """

    def test_different_orders(self):
        sequences = [['C', 'G', 'Am', 'F'], ['Am', 'F', 'C', 'G']]
        for order in [1, 2]:
            predictor = ChordPredictor(sequences, order=order)
            current_chords = ['G'] if order == 1 else ['G', 'Am']
            predictions = predictor.predict_chord(current_chords)
            assert predictions, f"在阶数为{order}时预测失败"
        print(f"不同阶数的预测测试通过,{predictions}")

    """
    测试在不同的阈值设置下，ChordPredictor是否能正确过滤掉低概率的预测结果。
    """

    def test_threshold_filtering(self):
        sequences = [['C', 'G', 'Am', 'F'], ['Am', 'F', 'C', 'G']]
        predictor = ChordPredictor(sequences, order=1)
        threshold = 0.5  # 设置一个较高的阈值，以确保过滤效果明显
        predictions = predictor.predict_chord(['C'], threshold=threshold)
        for _, prob in predictions:
            assert prob >= threshold, "存在低于阈值的预测结果"
        print(f"概率阈值过滤测试通过,{predictions}")

    """
    测试当输入的当前和弦少于模型阶数时，ChordPredictor应该如何处理。
    """

    def test_exception_for_insufficient_chords(self):
        sequences = [['C', 'G', 'Am', 'F'], ['Am', 'F', 'C', 'G']]
        predictor = ChordPredictor(sequences, order=2)
        try:
            predictor.predict_chord(['C'])  # 只有一个和弦，但模型的阶数为2
            raise AssertionError("应该抛出异常，因为当前和弦数量少于模型的阶数")
        except ValueError as e:
            print("异常情况测试通过:", e)

    """
    根据扩充的和弦序列调整测试用例
    """

    def test_extended_sequences(self):
        extended_sequences = [
            ['C', 'E', 'Am', 'F', 'G', 'C'],
            ['Am', 'G', 'F', 'Em', 'Dm', 'G', 'C'],
            ['F', 'G', 'Em', 'Am', 'Dm', 'G', 'C', 'F'],
            ['C', 'G', 'Am', 'F', 'Dm', 'Em', 'G', 'C'],
            ['Em', 'Am', 'Dm', 'G', 'C', 'F', 'Bdim', 'E'],
            ['G', 'D', 'Em', 'C', 'G', 'D', 'G'],
            ['A', 'D', 'E', 'F#m', 'D', 'A', 'E'],
            ['Bb', 'F', 'Gm', 'Eb', 'F', 'Bb', 'Gm', 'Eb'],
            ['Cm', 'G', 'Ab', 'Eb', 'Bb', 'Eb', 'Ab', 'G'],
            ['D', 'A', 'Bm', 'F#m', 'G', 'D', 'G', 'A']
        ]
        predictor = ChordPredictor(extended_sequences, order=1)
        current_chords = ['D']
        predictions = predictor.predict_chord(current_chords)
        assert predictions, "扩充和弦序列测试失败，预测结果为空"
        print(f"扩充和弦序列测试通过，预测结果非空, {predictions}")


if __name__ == '__main__':
    unittest.main()
