import csv

'''tests={'German': [u'Straße',u'auslösen',u'zerstören'],
       'French': [u'français',u'américaine',u'épais'],
       'Chinese': [u'中國的',u'英語',u'美國人']}

with open('utf.csv','w') as fout:
    writer=csv.writer(fout)
    writer.writerows([tests.keys()])
    for row in zip(*tests.values()):
        row=[s.encode('utf-8') for s in row]
        writer.writerows([row])
'''
def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        print(line["Name"]),
        print(line["Price"]),
        print(line["Link"])


if __name__ == "__main__":
    with open("projects_all.csv") as f_obj:
        csv_dict_reader(f_obj)