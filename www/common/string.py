import uuid

def gen_uuid():
    return uuid.uuid3(uuid.NAMESPACE_DNS, 'jianhu-www')

if __name__ == '__main__':
    print "gen_uuid: ", gen_uuid()