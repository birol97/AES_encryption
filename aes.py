import binascii
import re
import numpy as np
aes_sbox = [
    [int('63', 16), int('7c', 16), int('77', 16), int('7b', 16), int('f2', 16), int('6b', 16), int('6f', 16), int('c5', 16), int(
        '30', 16), int('01', 16), int('67', 16), int('2b', 16), int('fe', 16), int('d7', 16), int('ab', 16), int('76', 16)],
    [int('ca', 16), int('82', 16), int('c9', 16), int('7d', 16), int('fa', 16), int('59', 16), int('47', 16), int('f0', 16), int(
        'ad', 16), int('d4', 16), int('a2', 16), int('af', 16), int('9c', 16), int('a4', 16), int('72', 16), int('c0', 16)],
    [int('b7', 16), int('fd', 16), int('93', 16), int('26', 16), int('36', 16), int('3f', 16), int('f7', 16), int('cc', 16), int(
        '34', 16), int('a5', 16), int('e5', 16), int('f1', 16), int('71', 16), int('d8', 16), int('31', 16), int('15', 16)],
    [int('04', 16), int('c7', 16), int('23', 16), int('c3', 16), int('18', 16), int('96', 16), int('05', 16), int('9a', 16), int(
        '07', 16), int('12', 16), int('80', 16), int('e2', 16), int('eb', 16), int('27', 16), int('b2', 16), int('75', 16)],
    [int('09', 16), int('83', 16), int('2c', 16), int('1a', 16), int('1b', 16), int('6e', 16), int('5a', 16), int('a0', 16), int(
        '52', 16), int('3b', 16), int('d6', 16), int('b3', 16), int('29', 16), int('e3', 16), int('2f', 16), int('84', 16)],
    [int('53', 16), int('d1', 16), int('00', 16), int('ed', 16), int('20', 16), int('fc', 16), int('b1', 16), int('5b', 16), int(
        '6a', 16), int('cb', 16), int('be', 16), int('39', 16), int('4a', 16), int('4c', 16), int('58', 16), int('cf', 16)],
    [int('d0', 16), int('ef', 16), int('aa', 16), int('fb', 16), int('43', 16), int('4d', 16), int('33', 16), int('85', 16), int(
        '45', 16), int('f9', 16), int('02', 16), int('7f', 16), int('50', 16), int('3c', 16), int('9f', 16), int('a8', 16)],
    [int('51', 16), int('a3', 16), int('40', 16), int('8f', 16), int('92', 16), int('9d', 16), int('38', 16), int('f5', 16), int(
        'bc', 16), int('b6', 16), int('da', 16), int('21', 16), int('10', 16), int('ff', 16), int('f3', 16), int('d2', 16)],
    [int('cd', 16), int('0c', 16), int('13', 16), int('ec', 16), int('5f', 16), int('97', 16), int('44', 16), int('17', 16), int(
        'c4', 16), int('a7', 16), int('7e', 16), int('3d', 16), int('64', 16), int('5d', 16), int('19', 16), int('73', 16)],
    [int('60', 16), int('81', 16), int('4f', 16), int('dc', 16), int('22', 16), int('2a', 16), int('90', 16), int('88', 16), int(
        '46', 16), int('ee', 16), int('b8', 16), int('14', 16), int('de', 16), int('5e', 16), int('0b', 16), int('db', 16)],
    [int('e0', 16), int('32', 16), int('3a', 16), int('0a', 16), int('49', 16), int('06', 16), int('24', 16), int('5c', 16), int(
        'c2', 16), int('d3', 16), int('ac', 16), int('62', 16), int('91', 16), int('95', 16), int('e4', 16), int('79', 16)],
    [int('e7', 16), int('c8', 16), int('37', 16), int('6d', 16), int('8d', 16), int('d5', 16), int('4e', 16), int('a9', 16), int(
        '6c', 16), int('56', 16), int('f4', 16), int('ea', 16), int('65', 16), int('7a', 16), int('ae', 16), int('08', 16)],
    [int('ba', 16), int('78', 16), int('25', 16), int('2e', 16), int('1c', 16), int('a6', 16), int('b4', 16), int('c6', 16), int(
        'e8', 16), int('dd', 16), int('74', 16), int('1f', 16), int('4b', 16), int('bd', 16), int('8b', 16), int('8a', 16)],
    [int('70', 16), int('3e', 16), int('b5', 16), int('66', 16), int('48', 16), int('03', 16), int('f6', 16), int('0e', 16), int(
        '61', 16), int('35', 16), int('57', 16), int('b9', 16), int('86', 16), int('c1', 16), int('1d', 16), int('9e', 16)],
    [int('e1', 16), int('f8', 16), int('98', 16), int('11', 16), int('69', 16), int('d9', 16), int('8e', 16), int('94', 16), int(
        '9b', 16), int('1e', 16), int('87', 16), int('e9', 16), int('ce', 16), int('55', 16), int('28', 16), int('df', 16)],
    [int('8c', 16), int('a1', 16), int('89', 16), int('0d', 16), int('bf', 16), int('e6', 16), int('42', 16), int('68', 16), int(
        '41', 16), int('99', 16), int('2d', 16), int('0f', 16), int('b0', 16), int('54', 16), int('bb', 16), int('16', 16)]
]
rcon = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
keystring = "";
arx = [];
arp = [None] * 10
xxx = [];
#global variables for appending the keys into array
arr=[[],[],[],[],[],[],[],[],[],[],[]];

arr2=[[],[],[],[],[],[],[],[],[],[],[]];
def roundkey(keys,round1,keystring,first,text):
    if round1 == 0:
            
            first = keys
            xxx = keyexpansion(keys,round1,first)
            arr[round1] = xxx;
            round1 = round1 + 1
            return roundkey(xxx,round1,keystring,first,text)
    else:
        if round1 < 11 and round1 > 0:
                
                xx = keyexpansion(keys,round1,first)
                arr[round1] = xx;
                keystring.append(xx[:])
                round1 = round1 + 1
                return roundkey(keystring[round1-2],round1,keystring,first,text)
        else: 
                arr[0] = StateMatrix(first)
                
                x = "";
                for i in range(0,11):
                            
                    for z in range(0,16):
                        
                        count = 0;
                        if len(arr[i][z]) == 1:
                           arr[i][z] = "0"+str(arr[i][z])
                            
                        x = x + arr[i][z];
                        
                    arr2[i] = x;
                    x = "";
                
                        
                
                
                return encryption(text,0,arr2);
def ex(a,b):
        print("sdfsdf")
        return a + b
def StateMatrix(state):
        """ Formats a State Matrix str to a properly formatted list.
        """
        new_state = []
        split = re.findall('.' * 2, state)
        for x in range(4):
            new_state.append(split[0:4][x]); new_state.append(split[4:8][x])
            new_state.append(split[8:12][x]); new_state.append(split[12:16][x])
        return new_state
        """ rotation of rows are simple to implement so its hard codded.
        """
def Rotword(word):
        tmp = word[0];
        tmp3 = word[3];
        word[0] = word[1];
        word[3] = tmp;
        tmp2 = word[1];
        word[1] = word[2];
        word[2] = tmp3;     
        return word
        """ KEY_EXPANSION and SUBSTITUTE uses the S-Box
        the way it works getting the
        most significant nibble as the row, and the least 
        significant nibble as the columns
        """
def Subword(byte):
        
        x = byte >> 4
        y = byte & 15
             
     
            
        return aes_sbox[x][y] 
def getRcon(x):
         
        return Rcon[x]
        """Different types of xor functions are created 
        for different type of data types 
        """
def xor(first, last):
      
        column3= [];
        for i in range(0, 4):
            
            xxx = int(first[i],16) ^ last[i]
            
            column3.append(hex(xxx).lstrip("0x").rstrip("L"))
        
        return column3

def xorrc(first, last):
        
        column3= [];
        for i in range(0, 4):
            
            
            xxx = int(first[i],16) ^ int(last[i],16)
            
            if xxx == 0:
                xxx = "0"
                column3.append(xxx);
            else:
                
                column3.append(hex(xxx).lstrip("0x").rstrip("L"))
            
        return column3
    
         
def encryptionxor(first, last):
        s = "";
        for i in range(0,16):
            
            xxx = int(first[i],16) ^ int(last[i],16)
            if len(hex(xxx).lstrip("0x").rstrip("L")) == 0:
                    x1 = "00" + hex(xxx).lstrip("0x").rstrip("L")
                    s = s + x1
            else:  
            
                 if len(hex(xxx).lstrip("0x").rstrip("L")) < 2:
                    x1 = "0" + hex(xxx).lstrip("0x").rstrip("L")
                    s = s + x1
               
                 else:
                
                    s =   s + hex(xxx).lstrip("0x").rstrip("L")
               
        return s;
        """
    
        """
def shiftrows(state):
        x = state[1::4]
        
        y = state[2::4]
        
        z = state[3::4]
        
        
            
        tmp = x[0];
        x[0] = x[1];
        tmp1 = x[1];
        x[1] = x[2];
        x[2] = x[3]
        x[3] = tmp;
        state[1::4] = x;
        
            
        tmp = y[0]
        y[0] = y[2]
        tmp1 = y[1]
        y[1] = y[3];
        y[2] = tmp
        y[3] = tmp1
        state[2::4] = y;
     
        
        tmp11 = z[0]
        z[0] = z[3];
        tmp12 = z[1]
        z[1]  = tmp11
        z[3] = z[2];
        z[2]  = tmp12        
                
          
                
        state[3::4]  = z;     
        return state;
    
    
        
    
def keyexpansion(key,round,self):
        if round == 0:
            
            state = StateMatrix(key); #format the key as an matrix
            
            return state
        if round >0:
            state = key;
            column = state[3::4]
            x = state[3::4]
            z = Rotword(x) # rotates the row
        xx=[];#empty array is created for temp storage for keeping values after sub-byte process
        for i in z:
            g = hex(int(i,16))
            k = Subword(int(i,16))#New values are gathered from aes-sbox
            xx.append(hex(k))
        state[3::4] = xx # new values applied to the matrix
        current_rcon=[]
        xor_state=[]
        current_rcon.append(rcon[round])
        for i in range(1,4):
                current_rcon.append(0x00); #rcon values are modified depending on the round number
        xor_state = xor(state[3::4],current_rcon);#xor opeartions are made
        state[0::4] =  xorrc(state[0::4],xor_state)
        state[3::4] = column
        for i in range(1,4):
            
            state[i::4] =  xorrc(state[i-1::4],state[i::4])
        name = state
        return name # new key value in matrix format is returned
      
 
                   
         
            
        
def encryption(plaintext,roundx,key1):
        
        if roundx == 0:
            
            
            state = StateMatrix(plaintext)
            new_state= "";
            for i in range(0,16):
                new_state = new_state+state[i]
            state = StateMatrix(new_state)    
            
            
            key1[roundx] =  StateMatrix(key1[roundx])
            
           
            xx = encryptionxor(state,key1[roundx]) 
            
            roundx = roundx + 1;
            return encryption(xx,roundx,key1);
        else:
            new_state=[];### modified values added here            
            for i in range(0,16):
                    x = i * 2;
                    y = x + 1;
                    z = plaintext[x]+plaintext[y]  ## 2 values combined to get proper hex values to make understandble int format
                    g = hex(int(z,16))    ##subword function will find the corresponding values of int 
                    k = Subword(int(g,16)) 
                    if len(hex(k).lstrip("0x").rstrip("L")) < 2:
                        x1 = "0" + hex(k).lstrip("0x").rstrip("L") ##formating the values to understandable format
                        new_state.append(x1)      
                    else:    
                        new_state.append(hex(k).lstrip("0x").rstrip("L"));
            shiftrows(new_state)
            column1 = new_state[0:4]  ##each column is gathered into sub arrays
            column2 = new_state[4:8]
            column3 = new_state[8:12]
            column4 = new_state[12:16]
            for i in range(0,4):
                column1[i] =  int(column1[i],16)
            new_state[0:4] = mix_column(column1) # each values of the column modified with mix columns
            for i in range(0,4):       # and the new values are updated of the matrix
                column2[i] =  int(column2[i],16)
            new_state[4:8] = mix_column(column2)
            for i in range(0,4):
                column3[i] =  int(column3[i],16)
            new_state[8:12] = mix_column(column3)
            for i in range(0,4):
                column4[i] =  int(column4[i],16)
            new_state[12:16] = mix_column(column4)
            #################
            key1[roundx] =  StateMatrix(key1[roundx])
                                  ## key and modified plain text is 
            new_state = encryptionxor(new_state,key1[roundx])
            roundx = roundx + 1;
            
            
            if roundx < 11:
                return encryption(new_state,roundx,key1)
            else:
                new_state=[];            
                for i in range(0,16):
                    
                    x = i * 2;
                    y = x + 1;
                    
                    z = plaintext[x]+plaintext[y]
                    
                    
                    g = hex(int(z,16))
                    k = Subword(int(g,16))
                    if len(hex(k).lstrip("0x").rstrip("L")) < 2:
                        
                        x1 = "0" + hex(k).lstrip("0x").rstrip("L")
                        new_state.append(x1)
                    
                    else:    
                        new_state.append(hex(k).lstrip("0x").rstrip("L"));
                          
                   
            
                plaintext = shiftrows(new_state)
                plaintext = encryptionxor(plaintext,key1[roundx-1])
                return "ciphertext: "+ plaintext    
        """
        MixColumns operation are GF(2^8) multiplication operations
        Multiplying by fix constant(1,2,3) make our job easier to implement
        Multiplying 1 gives same output
        Multiplying 2 is equal to shift number left by one
        and then xoring with 1x1B  if the high bit is 1 
        if the high bit was a zero, then you don't need to 
        XOR anything 
        Multiplying 3
        This "addition" operation is actually XOR.
        """   
    
def multiply_by_2(v):
        s = v << 1
        s &= 0xff
        if (v & 128) != 0:
            s = s ^ 0x1b
        return s


def multiply_by_3(v):
        
        return multiply_by_2(v) ^ v


def mix_column(column):
        new_column = [
        str(hex(multiply_by_2(column[0]) ^ multiply_by_3(
            column[1]) ^ column[2] ^ column[3])),
        str(hex(multiply_by_2(column[1]) ^ multiply_by_3(
            column[2]) ^ column[3] ^ column[0])),
        str(hex(multiply_by_2(column[2]) ^ multiply_by_3(
            column[3]) ^ column[0] ^ column[1])),
        str(hex(multiply_by_2(column[3]) ^ multiply_by_3(
            column[0]) ^ column[1] ^ column[2])),
    ]
        for i in range(0,4):   
            if len(new_column[i].lstrip("0x").rstrip("L")) < 2:
                        
                        x1 = "0" + new_column[i].lstrip("0x").rstrip("L")
                        new_column[i] = x1;
                    
            else:    
                        x2 =  new_column[i].lstrip("0x").rstrip("L")
                        new_column[i] = x2;
        return new_column
        
    
if __name__ == '__main__':
       Key = input("Please enter the key") 
       Plaintext = input("Please enter the plaintext")
       arrs=[];
       plaintext =  '00000000000000000000000000000000'
       key = 'ffffffffffffffffffffffffffffffff'
       initial_round = 0;
       print(roundkey(Key,initial_round,arrs,initial_round,Plaintext))
       ex(Key,Plaintext)
       