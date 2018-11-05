import csv
rel3 = file('C:/Users/ZLL/Desktop/rel3.csv', 'wb')
writer = csv.writer(rel3)

rel = file('C:/Users/ZLL/Desktop/rel.csv', 'rb')
reader = csv.reader(rel)

for line in reader:
	linedata=(line[0],line[1])
	writer.writerows(linedata)
rel3.close() 