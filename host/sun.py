from planet import Planet
import game_engine

""" Default values (default, min, max)  """
__defaults = {
    'distance': [0, 0, 0]
}

""" TODO """
class Sun(Planet):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Sun, defaults=__defaults)

def test_expect(actual, expect, test_id):
    if expect != actual:
        print('ERROR ', test_id, ' got ', actual, ' expected ', expect)

""" TODO """
def _test():
    print('sun.test-start')
    s = Sun()
    test_expect(s.gravity, 50, 'sun_test #1')
    test_expect(s.temperature, 50, 'sun_test #2')
    test_expect(s.radiation, 50, 'sun_test #3')
    test_expect(s.player.is_valid, False, 'sun_test #4')
    test_expect(s.distance, 0, 'sun_test #5')
    print('sun.test-end')
