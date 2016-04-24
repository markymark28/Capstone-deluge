enig_builder = gtk.Builder()
read = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/loggedinusrs.txt", 'r')
i = 0
for line in read:
    i = i + 1
    if i%2 == 0:
        lvl = line.rstrip('\n')
        accesslevel = lvl
    else:
        usrname = line.rstrip('\n')
read.close
filepath = "/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/ui/gtkui/glade/" + str(accesslevel)     
enig_builder.add_from_file(filepath+"/starting_enigmail.ui")#resource_filename(
enig_window = enig_builder.get_object("window1")
enig_window.show_all()
