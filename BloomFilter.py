from BitHash import BitHash
from BitVector import BitVector

# equation A: P = (1-phi)^d
# equation B: phi = (1-P^(1/d))
# equation C: phi = (1 - d/N)^n
# equation D: N = d/(1-phi^(1/n))
# P = false positive rate
# d = numHashes
# n = numKeys

class BloomFilter(object):
    # Returns the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    # You use equation B to get the desired phi from P and d
    # You then use equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        #uses equation B to get phi from maxFalsePositive and numHashes
        phi = 1 - maxFalsePositive**(1/numHashes)
        
        #uses equation D to return numBits from phi and numKeys
        return (numHashes / (1-phi**(1/numKeys)))
        
    # Creates a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        
        #creates BloomFilter using a BitVector with size of bitsNeeded 
        self.__BloomFilter = BitVector(size = int(self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)))
        
        #stores number of bits that were set from inserting keys
        self.__numBitsSet = 0
        
        #stores number of hashes for each key
        self.__numHashes = numHashes

    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        
        #keeps track of how many times the key has been hashed
        i = 0
        
        #keeps track of starting seed, defaults to 0
        h = 0
        
        #hashes the key numHashes times
        while i < self.__numHashes:
            
            #hashes key and stores it in h to use as seed for next hash
            h = BitHash(key, h)
            
            #checks if bit has been set before
            if self.__BloomFilter[h%len(self.__BloomFilter)] == 0:
                
                #if not, then set it and increase numBitsSet
                self.__BloomFilter[h%len(self.__BloomFilter)] = 1
                self.__numBitsSet += 1
                
            #increase i to keep track of number of times key has been hashed
            i +=1
            
    # hash key d times if any are 0 then return false
    # if all 1 then return true
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        
        #keeps track of how many times the key has been hashed
        i = 0
        
        #keeps track of starting seed, defaults to 0        
        h = 0
        
        #hashes the key numHashes times        
        while i < self.__numHashes:
            
            #hashes key and stores it in h to use as seed for next hash            
            h = BitHash(key, h)
            
            #if bit is set to 0, then key must have not have been inserted into
            #BloomFilter so returns False
            if self.__BloomFilter[h%len(self.__BloomFilter)] == 0:
                return False
            
            #increase i to keep track of number of times key has been hashed            
            i +=1     
            
        #if looped through all the bits the key has hashed to and none was set to 0,
        #the ket may have been inserted into the BloomFilter so returns True
        return True  
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # actually measuring the proportion of false positives that 
    # are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        
        #solves for phi by subtracting the actual measured current proportion 
        # of bits in the bit vector that are 1 divided by the
        # num Bits in the Bloom Filter from 1
        phi = (1-((self.__numBitsSet )/ len(self.__BloomFilter)))
        
        #uses equation A to solve for falsePositiveRate using phi and numHashes
        return (1 - phi)**self.__numHashes
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        
        #returns the numbBitsSet that were setted whenever a key was 
        #inserted into BloomFilter
        return self.__numBitsSet     

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
   
    # creates the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalse)
    
    # opens the text file
    fin = open("wordlist.txt")
    
    # reads the first numKeys words from the file and insert them 
    # into the Bloom Filter.
    for i in range(numKeys):
        b.insert(fin.readline())
    
    #Close the input file.   
    fin.close()
    
    # Prints out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.

    print(b.falsePositiveRate())
    
    # Now re-open the file
    fin = open("wordlist.txt")
    
    #keeps track of how many words from the file are missing from the BloomFilter
    missing = 0
    
    #re-read the same bunch of the first numKeys and counts the missing
    for i in range(numKeys):
        if not b.find(fin.readline()):
            missing +=1
            
    #prints missing words from BloomFilter, should be 0!
    print(missing)
    
    #count how many of the words can be (falsely) found in the Bloom Filter
    falseFound = 0
   
               
    # reads the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter
    # if the word is found in the bloomFilter, increases
    # falseFound
    for i in range(numKeys):
        if b.find(fin.readline()):
            falseFound +=1
    
    # Prints out the percentage rate of false positives
    # should be close to the estimated false positive rate previously printed
    print(falseFound / numKeys)
    
    
if __name__ == '__main__':
    __main()       

