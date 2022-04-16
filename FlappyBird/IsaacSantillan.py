import unittest
# Functions we want to test  
def addnow(time,time2,freq):
    if time-time2>freq:
        return True 
    else:
        return False

def bgpos(x,y):
    if x<y:
        return True
    else:
        return False 

class TestSandbox2(unittest.TestCase):
    # if 20-5>3 then the test block should return True
    # We wanted to test this function in particular as it plays an important
    # ..part in checking when to add the next pipe and fireball in our game.
    #..if we didn't have this function then pipes/fireballs would be generated right after another and not
    #...allow the user to have time to react to the changes 
    def test_addnow(self):
        self.assertTrue(addnow(20,5,3))
        self.assertFalse(addnow(7,4,20))
    # if 7 is less than 14 then the test block should return True
    # Alought this block seems simple we wanted to test it because it determines when to scroll 
    #the background left. If the screen width is less than the end of the image then we know to 
    # ..generate a background image that immediately follows it  
    def test_bgpos(self):
        self.assertTrue(bgpos(7,14))

if __name__ == "__main__":
    unittest.main()


