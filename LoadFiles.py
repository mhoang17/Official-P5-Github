import glob, os, time
import pandas as pd


def read_files(path):
    all_files = glob.glob(path)
    csv_data_dict = {}
    count_of = 1

    print('\n[+] Running files.. please wait')
    start_file = time.time()  
    
    for filename in all_files:
        print('    ..' + filename + ' - ' + str(count_of) + ' of ' + str(len(all_files)))
        get_only_filename = os.path.basename(filename)
        only_filename = get_only_filename.replace('.csv','')
        df = pd.read_csv(filename, header=0, low_memory=False, encoding='utf-8' )
        csv_data_dict[only_filename] = df  # .apply(lambda x: x.astype(str).str.lower())
        count_of += 1
    end_file = time.time()
    
    print('    ... Total time reading files (s) = ' + str(end_file-start_file) + '\n')
    return csv_data_dict
