import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.prediction import Prediction


class TestPrediction(unittest.TestCase):

    def setUp(self):
        self.prediction = Prediction()

    def tearDown(self):
        self.prediction = None

    def test_predict_empty(self):
        question = ""
        context = ""
        self.assertEqual(self.prediction.predict(question, context), "empty")

    def test_predict_1(self):
        context = "A reusable launch system (RLS, or reusable launch vehicle, RLV) is a \
        launch system which is capable of launching a payload into space more than once. \
        This contrasts with expendable launch systems, where each launch vehicle is \
        launched once and then discarded. No completely reusable orbital launch \
        system has ever been created. Two partially reusable launch systems were \
        developed, the Space Shuttle and Falcon 9. The Space Shuttle was partially \
        reusable: the orbiter (which included the Space Shuttle main engines and the \
        Orbital Maneuvering System engines), and the two solid rocket boosters were \
        reused after several months of refitting work for each launch. The external \
        tank was discarded after each flight."
        question =  "How many partially reusable launch systems were developed?"
        self.assertEqual(self.prediction.predict(question, context), "Two")

if __name__ == '__main__':
    unittest.main()
