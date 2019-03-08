import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.ner.ner_babelfy import Ner_Babel


class TestNer(unittest.TestCase):

    def setUp(self):
        self.ner = Ner_Babel()

    def tearDown(self):
        self.ner = None

    def test_get_entities_empty(self):
        text = ""
        self.assertEqual(self.ner.get_entities(text), [])
    
    def test_get_entities_noone(self):
        text = "there is no entity here"
        self.assertEqual(self.ner.get_entities(text), [])


    def test_get_entities_0(self):
        text = "Did Uriah honestly think he could beat The Legend of Zelda in under three hours?"
        self.assertEqual(self.ner.get_entities(text)[0], "Uriah")

    # def test_get_entities_1(self):
    #     text = "What is Machine Learning ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Machine Learning")

    # def test_get_entities_2(self):
    #     text = "What are Genetic Algorithms ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Genetic Algorithms")

    # def test_get_entities_3(self):
    #     text = "What is Artificial Intelligence ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Artificial Intelligence")

    # def test_get_entities_4(self):
    #     text = "What is activation function ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "activation function")

    # def test_get_entities_5(self):
    #     text = "What is gradient descent ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "gradient descent")

    # def test_get_entities_6(self):
    #     text = "What is a generation ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "generation")

    # def test_get_entities_7(self):
    #     text = "What is Activation Function on Neural Networks ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Activation Function")

    # def test_get_entities_8(self):
    #     text = "What is Gradient Descent on Neural Networks ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Gradient Descent")

    # def test_get_entities_9(self):
    #     text = "What is a Generation in Genetic Algorithms ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Generation")

    # def test_get_entities_10(self):
    #     text = "Is Genetic Algorithms a subfield of Artificial Intelligence ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Genetic Algorithms")

    # def test_get_entities_11(self):
    #     text = "Is Neural Networks a subfield of Machine Learning ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Neural Networks")

    # def test_get_entities_12(self):
    #     text = "Is Data Mining related to Natural language Processing ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Data Mining")

    # def test_get_entities_13(self):
    #     text = "What Neural Networks are used for ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Neural Networks")

    # def test_get_entities_14(self):
    #     text = "How Convolutional Neural Networks work ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Convolutional Neural Networks")

    # def test_get_entities_15(self):
    #     text = "Is Generation the same as Epoch ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Generation")

    # def test_get_entities_16(self):
    #     text = "Is Generation the same as Epoch ?"
    #     self.assertEqual(self.ner.get_entities(text)[1], "Epoch")

    # def test_get_entities_17(self):
    #     text = "Is Data Mining related to Natural language Processing ?"
    #     self.assertEqual(self.ner.get_entities(text)[1], "Natural language Processing")

    # def test_get_entities_18(self):
    #     text = "Is Activation Function part of Neural Network ?"
    #     self.assertEqual(self.ner.get_entities(text)[0], "Activation Function")







if __name__ == '__main__':
    unittest.main()
