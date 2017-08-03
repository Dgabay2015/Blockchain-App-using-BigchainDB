from bigchaindb_driver.crypto import generate_keypair

class Key:

    def __init__(self):
        self.key = generate_keypair()

    def getkey(self):
        return self.key


aliceo = Key()
alice = aliceo.getkey()

bobo = Key()
bob = aliceo.getkey()