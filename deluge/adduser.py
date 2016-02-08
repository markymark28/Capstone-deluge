import hashlib

#pwd file
f = open('hashes.txt', 'w')	
hash_object = hashlib.md5(b'operator')
f.write("%s\n" % hash_object.hexdigest())
f.write("operator")
f.close()

#usrname file
f = open('usrnames.txt', 'w')
hash_object = hashlib.md5(b'Bayless')
f.write("%s\n" % hash_object.hexdigest())
f.close()
