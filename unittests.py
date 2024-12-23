import unittest
from io import StringIO
import json
from hw3 import parse_dictionary

class TestParseDictionary(unittest.TestCase):
    def test_basic_conversion(self):
        input_text = '{ name => "Ivan", age => 30, address => "Moscow" }'
        expected_output = {"name": "Ivan", "age": 30, "address": "Moscow"}
        self.assertEqual(parse_dictionary(input_text), expected_output)

    def test_with_comments(self):
        input_text = '<!-- Comment --> { name => "Alex", age => 25, city => "Novosibirsk" } // Inline comment'
        expected_output = {"name": "Alex", "age": 25, "city": "Novosibirsk"}
        self.assertEqual(parse_dictionary(input_text), expected_output)

    def test_with_array(self):
        input_text = '{ hobbies => #("reading", "coding", "gaming") }'
        expected_output = {"hobbies": ["reading", "coding", "gaming"]}
        self.assertEqual(parse_dictionary(input_text), expected_output)

    def test_variable_assignment(self):
        input_text = '{ name => "Kostya", age => 19, sport => "Football" }'
        expected_output = {'name': 'Kostya', 'age': 19, 'sport': 'Football'}
        self.assertEqual(parse_dictionary(input_text), expected_output)

    def test_invalid_syntax(self):
        input_text = '{ age => 80, address => "Italia", : "Mia", food => "Pizza" }'
        with self.assertRaises(SyntaxError):
            parse_dictionary(input_text)

    def test_unicode_characters(self):
        input_text = '{ name => "Ванёк", age => 31, address => "МСК" }'
        expected_output = {"name": "Ванёк", "age": 31, "address": "МСК"}
        self.assertEqual(parse_dictionary(input_text), expected_output)

if __name__ == "__main__":
    unittest.main()
