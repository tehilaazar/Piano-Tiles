import random
import time
from BitHash import BitHash, ResetBitHash

#creates a link class to store the key and data
class Link(object):
    def __init__(self, k, d):
        self.key  = k
        self.data = d

#creates cuckooHashing data structure class that resolves collisions in 
#hash tables. There are two hash tables of equal size with two seperate 
#hash functions.
class CuckooHashing(object):
    
    def __init__(self, numBuckets):
        
        #initializes the two hashtables of equal size        
        self.__hashTab1 = [None] * numBuckets
        self.__hashTab2 = [None] * numBuckets
       
        #stores current number of keys in both tables
        self.__numRecords = 0   
    
    #prints out the two hashTables
    def __str__(self):
        tab1 = tab2 = "["
        for i in range(len(self.__hashTab1)-1):
            if self.__hashTab1[i]: tab1 += str(self.__hashTab1[i].key) + ":" + str(self.__hashTab1[i].data) + ","
            if self.__hashTab2[i]: tab2 += str(self.__hashTab2[i].key) + ":" + str(self.__hashTab2[i].data) + ","
            if not self.__hashTab1[i]: tab1+= "None,"
            if not self.__hashTab2[i]: tab2+= "None,"
        if self.__hashTab1[-1]: tab1 += str(self.__hashTab1[-1].key) + ":" + str(self.__hashTab1[-1].data) 
        if self.__hashTab2[-1]: tab2 += str(self.__hashTab2[-1].key) + ":" + str(self.__hashTab2[-1].data)
        if not self.__hashTab1[-1]: tab1+= "None"
        if not self.__hashTab2[-1]: tab2+= "None"
        tab1 += "]"
        tab2 += "]"
        return tab1 + tab2
    
    #given a key, checks if it is in either hash table- it can only
    #be in one nest. If key is found, returns nest where key should be, 
    #link where key was found, and the which hash table the nest and link are from
    def __findLink(self, key):
        
        #uses first hash function to see what key hashes to for first hash table 
        hash1 = BitHash(key)
        
        #find the nest it hashes to by moding it by the length of the hashTable 
        nest1 = hash1 % (len(self.__hashTab1))
        
        #uses second hash function to see what nest it hashes to for second hash table
        nest2 = BitHash(key, hash1) % (len(self.__hashTab2))
        
        #checks the nests in the hashtables to see if either is full and has the
        #correct key. If it does, it returns the data. If not, it returns None
        #Note: only one hashtable could hold the key/data pair
        link1 = self.__hashTab1[nest1] 
        link2 = self.__hashTab2[nest2]
        
        #returns a tuple of numHashtable, which nest, and which link
        if link1 and link1.key == key: return 1, nest1, link1
        elif link2 and link2.key == key : return 2, nest2, link2
        
        #if the link is None, returns a tuple of Nones
        return None, None, None
        
    #given a key, uses __findLink to get the link. If there is data
    #returns it, otherwise returns None.
    def find(self, key):
        numHashTable, nest, link = self.__findLink(key)
        return link.data if link and link.key == key else None        
    
    #given a key, uses __findLink to get the link. If if is not None,
    #deletes the link from the hashTable and returns it, if can't find link,
    #returns None
    def delete(self, key):
        numHashTable, nest, link = self.__findLink(key)
        if link and link.key == key:
            self.__numRecords -= 1  
            if numHashTable == 1:
                (self.__hashTab1)[nest] = None
            else:
                (self.__hashTab2)[nest] = None
            return link
        return None
    
    #if the hashtables get too big, namely 50% full (together), then growHashTable
    #is invoked. It doubles the size of each hash table and rehashes each link 
    #into its new nest.
    def growHashTable(self):

        #creates list same size as current hashtables to double the hashtables
        addOnList = [None]*len(self.__hashTab1)
        self.__hashTab1.extend(addOnList)
        self.__hashTab2.extend(addOnList)
        
        #calls reinsert to loop through both hashtables and reinsert each link into proper nest
        self.reInsert(len(addOnList))
    
    #when there's a loop of 16 times, each link has to be reinserted
    #into the hashTables
    #method used by growHashTable and reHash to reinsert all the nests after growing
    #or changing the hash function
    def reInsert(self, len):
        
        #resets the numRecords because reinserts each link
        self.__numRecords = 0
        
        #loops through each hashtable and reinserts each link into proper nest
        for j in range(len):
            key = ((self.__hashTab1)[j]).key if (self.__hashTab1)[j] else None
            data = ((self.__hashTab1)[j]).data if (self.__hashTab1)[j] else None
            key2 = ((self.__hashTab2)[j]).key if (self.__hashTab2)[j] else None
            data2 = ((self.__hashTab2)[j]).data if (self.__hashTab2)[j] else None
            
            #resets old location to None
            self.__hashTab1[j] = None
            self.__hashTab2[j] = None  
            
            #inserts the keys into their new nests!
            self.insert(key, data) if key else None
            self.insert(key2, data2) if key2 else None        
        
    def resetHash(self):
    
        #calls method to change the hash function
        ResetBitHash()

        #calls reinsert to loop through each hashtable and reinsert each link into proper nest
        self.reInsert(len(self.__hashTab1))
        
    #returns how dense the hashtables are      
    def howDense(self):
        return self.__numRecords / (self.len()*2)
    
    #returns the length of each hash table (which is the same)
    def len(self):
        return len(self.__hashTab1)
    
    #returns the number of records in the hashTables
    def numRecords(self):
        return self.__numRecords
    
    #when a key/data pair is being inserted it goes into the first hash
    #table at the value. If there is something there, it evicts it, and 
    #the node there is then entered into hashtab2. If there is something
    #in nest where try to put key in hashtab2, evicts that. Returns True after
    #key/data pair has been inserted 
    def insert(self, key, data):
        
        #if the key already exists in either hashtable, 
        #replaces old data with new data and returns out of insert 
        hash1 = BitHash(key) 
        nest1 = hash1 % len(self.__hashTab1)
        nest2 = BitHash(key, hash1) % (len(self.__hashTab2))
        
        #if key exists already in hashtable
        if self.__hashTab1[nest1] and key == (self.__hashTab1[nest1]).key: 
            
            #replaces the data
            self.__hashTab1[nest1].data = data
            return True
        
        #if key exists already in hashtable        
        elif self.__hashTab2[nest2] and key == (self.__hashTab2[nest2]).key: 
            
            #replaces the data
            self.__hashTab2[nest2].data = data
            return True
        
        #create variable to keep track of loop where no nest is open and the links
        #keep being evicted from nests. If it loops for more than 16 times, and hashtables
        #are more than 60% dense, then grows hash tables. If not dense enough, rehashes.
        i = 0
        
        #create value to keep track of which hashtable to insert into
        ht = 1
        
        while i<16:
            
            #if up to first hashTable..
            if ht==1:
                #store the key/data pair at the nest in the hashTable 
                #if doesn't exist then it's None
                temp = self.__hashTab1[nest1] 
            
                #put the new link being inserted into the ht hashtable
                self.__hashTab1[nest1] = Link(key, data)
                
                #if first time through loop, then new Link is being inserted 
                #and increases numRecords
                if i==0:
                    self.__numRecords += 1         
            
            #if up to second hashTable..
            elif ht==2:
                #store the key/data pair at the nest in the hashTable 
                #(if doesn't exist then it's None)
                temp = self.__hashTab2[nest2] 
            
                #put the new link being inserted into the ht hashtable
                self.__hashTab2[nest2] = Link(key, data)
           
                #if first time through loop, then new Link is being inserted 
                #and increases numRecords                
                if i==0:
                    self.__numRecords += 1         
            
            #check if temp exists and is not None, if it exists that means 
            #there was a link in that nest in hashtable. if it is None
            #then new link was inserted into empty nest and can return True
            if not temp: return True
            if temp:
                key = temp.key
                data = temp.data
                hash1 = BitHash(key)
                nest1 = hash1 % len(self.__hashTab1)
                nest2 = BitHash(key, hash1) % (len(self.__hashTab2))
                
                i+=1 
                ht += 1
                if ht==3: ht=1
           
        #if exiting while loop that means it has looped 16 times and now gonna check
        #how dense the hashtables are, if at least 60% full then gonna grow hashtable, if less,
        #gonna rehash.     
        if self.howDense() >= .6:
            #calls growHash
            self.growHashTable()
            
            #tries to insert the key/data again
            self.insert(key, data)      
            
        else: 
            #calls rehash            
            self.resetHash()
            
            #tries to insert the key/data again            
            self.insert(key, data)
                    
  