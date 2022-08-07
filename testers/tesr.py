import unittest
import utils, copyworld2


class MyTestCase(unittest.TestCase):
    #def test_something(self):
       # utils.copy_dir(r'C:\Users\tsrow\curseforge\minecraft\Instances\GT New Horizons\saves\Bitch', r'H:\My Drive\Minecraft')

    def test_paths(self):
        copyworld.pack_or_world("C:/Users/tsrow/curseforge/minecraft/Instances", "bitch")



if __name__ == '__main__':
    unittest.main()
