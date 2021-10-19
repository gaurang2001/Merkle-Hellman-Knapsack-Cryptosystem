from random import randint, shuffle

class MerkleHellman:

    def __init__(self):
        self.w = []  # Private Key
        self.q = 0
        self.r = 0
        self.b = []  # Public Key
        self.maxcharacters = 200
        self.maxbinarylength = self.maxcharacters*8
        self.generate_keys()


    def generate_keys(self):
        maxnumberofbits = 50
        sum = 0
        for i in range(self.maxbinarylength):
            self.w.append(sum + randint(1,2**maxnumberofbits))
            sum += self.w[i]

        # shuffle(self.w)                   ################ Use for Hard Knapsack

        self.q = sum + randint(1,2**maxnumberofbits)
        self.r = self.q-1
        for i in range(self.maxbinarylength):
            self.b.append((self.w[i]*self.r)%self.q)

    def encrypt(self, message):
        binarymessage = ""
        for letter in message:
              binarymessage += (bin(ord(letter)).lstrip("0b")).zfill(8)

        if len(binarymessage) < self.maxbinarylength:
              binarymessage = binarymessage.zfill(self.maxbinarylength)
  
        cipher = 0
        for i in range(0,len(binarymessage)):
            cipher += self.b[i]*int(binarymessage[i],2)
  
        return cipher


    def egcd(self,a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self,a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return (x%m + m) % m

    def decrypt(self, cipher):
        plaintext = ""
        binarystring = ""
        cipherint = cipher
        modularinverse = self.modinv(self.r,self.q)
        inversecipher = (cipherint*modularinverse)%self.q
        for i in range(len(self.w)-1,-1,-1):
            if self.w[i] <= inversecipher:
                inversecipher -= self.w[i]
                binarystring += "1"
            else:
                binarystring += "0"

        binarystring = binarystring[::-1]
        for i in range (0,len(binarystring),8):
            letter = binarystring[i:i+8]
            check = int(letter,2)
            if check != 0:
                plaintext += chr(check)
    
        return plaintext            
            

if __name__ == "__main__":
     
    obj = MerkleHellman()

    message = input("Enter plain text to be encrypted:\n > ")
    print("\n\n")

    encrypted = obj.encrypt(message)
    decrypted = obj.decrypt(encrypted)

    print("Encrypted message: ", encrypted, "\n\n\n")
    print("Decrypted message: ", decrypted)
