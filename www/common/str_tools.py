import uuid

def gen_uuid():
    return uuid.uuid3(uuid.NAMESPACE_DNS, 'jianhu-www')

def gen_short_uuid():
    uuid_str = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'jianhu-www'))
    return uuid_str.replace('-', '')

if __name__ == '__main__':
    print "gen_uuid: ", gen_uuid()
    print "gen_short_uuid: ", gen_short_uuid()