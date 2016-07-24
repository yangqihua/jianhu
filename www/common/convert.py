def str_to_int(str, default=0):
    try:
        return int(str)
    except Exception, e:
        return default

resource_url_base = "http://res.jianhu.com"

def get_resource_url():
    pass

if __name__ == '__main__':
    print "Test str_to_int: ", str_to_int("123")
    print "Test str_to_int: ", str_to_int("123", 1)
    print "Test str_to_int: ", str_to_int("a123")
    print "Test str_to_int: ", str_to_int("a123", 1)