import csv

class WriterManager:
    def __init__(self, file_name, header=False):
        self.__file = open(file_name, 'w')
        if not header:
            self.__writer = csv.writer(self.__file)
        else:
            self.__writer = csv.DictWriter(self.__file, fieldnames=header)
            self.__writer.writeheader()    
    def write_row(self, row):
        self.__writer.writerow(row)
    def flush(self):
        self.__file.flush()
    def __del__(self):
        self.__file.close()