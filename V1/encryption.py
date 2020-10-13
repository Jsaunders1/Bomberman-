#Bitwise Operations that are needed
def xor(a1, a2):
    result = int(a1, 2) ^ int(a2, 2)
    result = bin(result)[2:]
    result.zfill(32)
    return result

def And(a1, a2):
    result = int(a1, 2) & int(a2, 2)
    result = bin(result)[2:]
    result.zfill(32)
    return result

def Or(a1, a2):
    result = int(a1, 2) | int(a2, 2)
    result = bin(result)[2:]
    result.zfill(32)
    return result

def Not(a1):
    result = int(a1, 2) ^ int(2**32 - 1)
    result = bin(result)[2:]
    result.zfill(32)
    return result

def Add(a1, a2):
    result = int(a1,2) + int(a2,2)
    result = bin(result)[2:]
    result = result[:32]
    return result
    
def leftTurn(l, a):
    result = 1[a:] + 1[:a]
    result.zfill(32)
    return result

def lShift(l, a):
    result = int(1,2) <<a
    result = bin(result)[2:]
    return result

def hashing(message): #Constants 
    h0 = "10001110101010111010110011000111"
    h1 = "11101010101101011010101110001001"
    h2 = "10011111111100011101000101101110"
    h3 = "11110011011100100101010001110110"
    h4 = "11000011110100111110000100010000"

    bitMessage = ""
    for character in message:

        
        characterInBits = bin(ord(character))[2:].zfill(8) #Turn each letter into an 8 bit number

        bitMessage += characterInBits

    messageLength = len(message)

    bitMessage += "10000000"

    
    while len(bitMessage) % 512 != 448: #Add zeroes to the end until it is 64 away from a multiple of 512
        bitMessage += "0"


    bitMessage += bin(messageLength)[2:].zfill(64)#Add length of message as a 64 bit number
                                                  #Message is now a multiple of 512


    messageChunks = [bitMessage[i: i+512] for i in range(0, len(bitMessage), 512)]#Split into 512 chunks

    for chunk in messageChunks:
        w = ["0" for _ in range(80)]
        
        w[0: 15] = [chunk[i: i+32] for i in range(0, len(chunk), 32)]#Break into 32 bit groups

       
        i = 16  #Make into 80 32 groups
        while i < 80:
            w[i] = xor(xor(w[i-3], w[i-8]),
                       xor(w[i-14], w[i-16]))

            
            w[i] = leftTurn(w[i], 1)#Turn result by 1

            i += 1

        a = u0
        b = u1
        c = u2
        d = u3	
        e = u4

        #Process data
        i = 0
        while i < 80:
            if 0 <= i <= 19:
                f = And(Not(b), d)
                f = Or(And(b,c), f)
                k = "01010101111010010101011010101001"

            elif 20 <= i <= 39:
                f = xor(b, c)
                f = xor(f, d)
                k = "01101111110110011110101110101101"

            elif 40 <= i <= 59:
                f = And(b, d)
                f = Or(f, And(b, c))
                f = Or(f, And(c, d))
                k = "10001111000110000100110011011100"

            elif 60 <= i <= 79:
                f = xor(b, c)
                f = xor(f, d)
                k = "11001010011000101100000111111001"

            temp = Add(leftTurn(a, 5), Add(Add(Add(k, w[i]), e), f))
            e = d
            d = c
            c =leftTurn(b, 30)
            b = a
            a = temp

            i += 1

        
        u0 = Add(u0, a)
        u1 = Add(u1, b)
        u2 = Add(u2, c)
        u3 = Add(u3, d)
        u4 = Add(u4, e)

    
    result = u0+u1+u2+u3+u4 #Add results for answer
    return hex(int(result,2))[2:-1]











    
