import csv

with open('dist_list.csv', 'wb') as csvfile:
    fieldnames = ['toggle_box', 'last_name','email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'toggle_box': False, 'last_name': 'Bayless', 'email': 'bayless.deluge@gmail.com'})
    writer.writerow({'toggle_box': False, 'last_name': 'Smith', 'email': 'smith.deluge@gmail.com'})
