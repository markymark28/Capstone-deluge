import hashlib

#pwd file
f = open('hashes.txt', 'w')

#user 1
hash_object = hashlib.md5(b'Bayless')
f.write("%s\t" % hash_object.hexdigest())	
hash_object = hashlib.md5(b'beatarmy')
f.write("%s\t" % hash_object.hexdigest())
f.write("operator\n")

#user 2
hash_object = hashlib.md5(b'Gumpert')
f.write("%s\t" % hash_object.hexdigest())
hash_object = hashlib.md5(b'gonavy')
f.write("%s\t" % hash_object.hexdigest())
f.write("maintenance\n")

#user 3                                                                                                                                                      
hash_object = hashlib.md5(b'Mark')
f.write("%s\t" % hash_object.hexdigest())
hash_object = hashlib.md5(b'blarg')
f.write("%s\t" % hash_object.hexdigest())
f.write("admin\n")
f.close()

