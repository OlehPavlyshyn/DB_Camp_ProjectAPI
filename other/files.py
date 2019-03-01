import csv
from DataGenerator.generator import dir




def write_to_csv(filename, list):
    dirr = dir() + 'DataGenerator/OutputData/' + filename + '.csv'
    try:
        with open(dirr, 'w') as f:
            wr = csv.writer(f, delimiter='\t')
            wr.writerows(list)
        res = 'file: ' + filename + ' deleted successfully'
    except:
        res = 'some error'
    return res


def clear_file(filename, list):
    dirr = dir() + 'DataGenerator/OutputData/' + filename + '.csv'
    try:
        with open(dirr , 'w') as f:
            for item in list:
                f.write("%s\t" % item)
        res = 'file: ' + filename + ' deleted successfully'
    except:
        res = 'some error'
    return res