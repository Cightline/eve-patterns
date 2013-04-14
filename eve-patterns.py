import os
import csv


class Pattern():
    def __init__(self):
        self.data = None
        self.log_path = "%s\Documents\EVE\logs\Marketlogs" % (os.environ["HOME"])
        self.data = {}
        
    def read_data(self, path):
        index = 0
        current_key = None
        
        with open(path, "r") as data:
            csv_data = csv.reader(data)

            print "importing.."
            # Strip empty keys and save them
            for row in csv_data:
                if index == 0:
                    for item in row:
                        if item != "":
                            self.data[item] = []
                            
                # c is the index of the key, and we can use it
                # to tell what piece of data we are looking at
                # as long as everything stays in order. 
                self.data[self.keys[index]].append(row[index])
                
                index += 1            

            
        

        

    def import_data(self):
        
        for f in os.listdir(self.log_path):
            if f[0:9] == "My Orders":
                self.read_data("%s\%s" % (self.log_path, f))




P = Pattern()
P.import_data()
