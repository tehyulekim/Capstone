import unittest
from . import fire1



class TestFire1(unittest.TestCase):
    def test1(self):
        self.assertTrue(True)

    def test2(self):
        self.assertTrue(False)

    def test3(self):
        print("fire1.f3() = ", fire1.f3())
        self.assertTrue(fire1.f3() == 3)

    def test4(self):
        print("fire1.f4() = ", fire1.f4())
        self.assertTrue(fire1.f4() == 4)


if __name__ == '__main__':
    unittest.main()
