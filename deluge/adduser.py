import hashlib

#pwd file
f = open('hashes.txt', 'w')

#user 1
f.write("Bayless:")
#hash_object = hashlib.md5(b'Bayless')
#f.write("%s\t" % hash_object.hexdigest())	
hash_object = hashlib.md5(b'beatarmy')
f.write("%s:" % hash_object.hexdigest())
f.write("operator\n")

#user 2
f.write("Gumpert:")
#hash_object = hashlib.md5(b'Gumpert')
#f.write("%s\t" % hash_object.hexdigest())
hash_object = hashlib.md5(b'gonavy')
f.write("%s:" % hash_object.hexdigest())
f.write("maintenance\n")

#user 3                                                                                                                                                      
f.write("Mark:")
#hash_object = hashlib.md5(b'Mark')
#f.write("%s:" % hash_object.hexdigest())
hash_object = hashlib.md5(b'blarg')
f.write("%s:" % hash_object.hexdigest())
f.write("admin\n")
f.close()

