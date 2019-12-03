import glob, os, time
import pandas as pd


def read_Files(path):
    all_files = glob.glob(path)
    csv_Data_Dict = {}
    count_Of = 1

    print('[+] Running files.. please wait')
    start_File = time.time()  
    
    for filename in all_files:
        print('    ..' + filename +' - '+ str(count_Of) +' of '+ str(len(all_files)))
        Get_Only_FileName = os.path.basename(filename)
        Only_FileName = Get_Only_FileName.replace('.csv','')
        df = pd.read_csv(filename, header=0, low_memory=False, encoding='utf-8' )
        csv_Data_Dict[Only_FileName] = df #.apply(lambda x: x.astype(str).str.lower())
        count_Of += 1
    end_File = time.time()
    
    print('    ... Total time reading files (s) = ' + str(end_File-start_File) + '\n')
    return csv_Data_Dict

    