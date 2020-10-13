#Bitwise xor
def xor(n1, n2):
    return bin(int(n1, 2) ^ int(n2, 2))[2:].zfill(32)

#Bitwise and
def bitAnd(n1, n2):
    return bin(int(n1, 2) & int(n2, 2))[2:].zfill(32)

#Bitwise or
def bitOr(n1, n2):
    return bin(int(n1, 2) | int(n2, 2))[2:].zfill(32)

#Bitwise not
def bitNot(n1):
    return bin(int(n1, 2) ^ (2**32 - 1))[2:].zfill(32)

#Bitwise add
def bitAdd(n1, n2):
    return bin(int(n1, 2) + int(n2, 2))[2:][:32]

#Rotate bits
def leftRotate(l, n):
    return l[n:] + l[:n].zfill(32)

#Left Shift
def lShift(l, n):
    return bin(int(l, 2) << n)[2:]

def sha(msg):
    #Predefined constants 
    h0 = "01100111010001010010001100000001"
    h1 = "11101111110011011010101110001001"
    h2 = "10011000101110101101110011111110"
    h3 = "00010000001100100101010001110110"
    h4 = "11000011110100101110000111110000"

    #Convert into bits
    bitMsg = ""
    for c in msg:

        #Get each character as an 8 bit number
        characterInBits = bin(ord(c))[2:].zfill(8)

        #Append it to message in bits
        bitMsg += characterInBits

    messageLength = len(msg)

    bitMsg += "10000000"

    #Add zeroes to the end until it is 64 away from a multiple of 512
    while len(bitMsg) % 512 != 448:
        bitMsg += "0"

    #Add length of message as a 64 bit number
    #Message is now a multiple of 512
    bitMsg += bin(messageLength)[2:].zfill(64)

    #Split into 512 bit chunks
    msgChunks = [bitMsg[i: i+512] for i in range(0, len(bitMsg), 512)]

    for chunk in msgChunks:
        w = ["0" for _ in range(80)]
        #Break chunk into 32 bit segments
        w[0: 15] = [chunk[i: i+32] for i in range(0, len(chunk), 32)]

        #Extend w to 80 32 bit segments
        for i in range(16, 79):
            #xor all the values together
            w[i] = xor(xor(w[i-3], w[i-8]),
                       xor(w[i-14], w[i-16]))

            #Rotate result by 1
            w[i] = leftRotate(w[i], 1)

        a = h0
        b = h1
        c = h2
        d = h3	
        e = h4

        #Process all the data
        for i in range(0, 79):
            if 0 <= i <= 19:
                f = bitOr(bitAnd(b, c), bitAnd(bitNot(b), d))
                k = "01011010100000100111100110011001"

            elif 20 <= i <= 39:
                f = xor(xor(b, c), d)
                k = "01101110110110011110101110100001"

            elif 40 <= i <= 59:
                f = bitOr(bitOr(bitAnd(b, c), bitAnd(b, d)), bitAnd(c, d))
                k = "10001111000110111011110011011100"

            elif 60 <= i <= 79:
                f = xor(xor(b, c), d)
                k = "11001010011000101100000111010110"

            temp = bitAdd(leftRotate(a, 5), bitAdd(bitAdd(bitAdd(k, w[i]), e), f))
            e = d
            d = c
            c =leftRotate(b, 30)
            b = a
            a = temp

        
        h0 = bitAdd(h0, a)
        h1 = bitAdd(h1, b)
        h2 = bitAdd(h2, c)
        h3 = bitAdd(h3, d)
        h4 = bitAdd(h4, e)

    #Get final result by appending the data together
    result = bitOr(bitOr(bitOr(bitOr(lShift(h0,128), lShift(h1,96)),
                               lShift(h2, 64)), lShift(h3, 32)), h4)

    #Final result        
    return hex(int(result,2))[2:-1]











    
