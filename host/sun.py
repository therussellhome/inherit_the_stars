from planet import Planet

class sun(Planet):
    pass

def test_expect(actual, expect, test_id):
    if expect != actual:
        print('ERROR ', test_id, ' got ', actual, ' expected ', expect)

def test():
    print('sun.test-start')
    s = sun()
    test_expect(s.gravity, 50, 'sun_test #1')
    test_expect(s.tempiter, 50, 'sun_test #1')
    test_expect(s.radeation, 50, 'sun_test #1')
    test_expect(s.player, None, 'sun_test #1')
    print('sun.test-end')
