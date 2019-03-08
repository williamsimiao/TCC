import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.ner.ner_simple import Ner_Simple


class TestNer(unittest.TestCase):

    def setUp(self):
        self.ner = Ner_Simple()

    def tearDown(self):
        self.ner = None

    def test_get_entities_empty(self):
        text = ""
        self.assertEqual(self.ner.get_entities(text), [])

    def test_get_entities_1(self):
        text = "Did Uriah honestly think he could beat The Legend of Zelda in under three hours?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Uriah")

    # def test_get_entities_2(self):
    #     text = "Is Machine Learning related to Artificial Inteligence?"
    #     self.assertEqual(self.ner.get_entities(text)[0][0], "Machine Learning")
    #
    # def test_get_entities_3(self):
    #     text = "What is a Neural Network?"
    #     self.assertEqual(self.ner.get_entities(text)[0][0], "Neural Network")
    #
    # def test_get_entities_4(self):
    #     text = "What is a Neural Machine Network?"
    #     self.assertEqual(self.ner.get_entities(text)[0][0], "Neural Machine Network")
    #
    # def test_get_entities_4(self):
    #     text = "Activation Function is part of Neural Network ?"
    #     self.assertEqual(self.ner.get_entities(text)[0][0], "Activation Function")

    def test_get_entities_1(self):
        text = "What is Machine Learning ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Activation Function")

    def test_get_entities_2(self):
        text = "What are Genetic Algorithms ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Activation Function")

    def test_get_entities_3(self):
        text = "What is Artificial Intelligence ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Activation Function")

    def test_get_entities_4(self):
        text = "What is activation function ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Activation Function")

    def test_get_entities_5(self):
        text = "What is gradient descent ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Activation Function")

    def test_get_entities_6(self):
        text = "What is a generation ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Activation Function")

    def test_get_entities_7(self):
        text = "What is activation function on Neural Networks ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Activation Function")

    def test_get_entities_8(self):
        text = "What is Gradient Descent on Neural Networks ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Gradient descent")

    def test_get_entities_9(self):
        text = "What is a Generation Genetic Algorithms ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Generation")

    def test_get_entities_10(self):
        text = "Is Genetic Algorithms a subfield of Artificial Intelligence ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Genetic Algorithms")

    def test_get_entities_11(self):
        text = "Is Neural Networks a subfield of Machine Learning ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Neural Networks")

    def test_get_entities_12(self):
        text = "Is Data Mining related to Natural language Processing ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Data Mining")

    def test_get_entities_13(self):
        text = "What Neural Networks are used for ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Neural Networks")

    def test_get_entities_14(self):
        text = "How Convolutional Neural Networks work ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Convolutional Neural Networks")

    def test_get_entities_15(self):
        text = "Is Generation the same as Epoch ?"
        self.assertEqual(self.ner.get_entities(text)[0][0], "Generation")





if __name__ == '__main__':
    unittest.main()
