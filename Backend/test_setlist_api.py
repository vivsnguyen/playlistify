from .. import setlist_api
import unittest

class MyAppUnitTestCase(unittest.TestCase):

    def test_adder(self):
        assert model.adder(2, 3) == 5

if __name__ == '__main__':
    unittest.main()