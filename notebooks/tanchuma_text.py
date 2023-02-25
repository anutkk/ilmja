import json
import re 
import os.path
from collections.abc import Iterable
from sklearn.model_selection import train_test_split



def get_data(test_size = 0.1 , permitted_characters = "אבגדהוזחטיכךלמםנןסעפףצץקרשת ' \"", random_state = 42):
    
    def flatten(xs):
        for x in xs:
            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                yield from flatten(x)
            else:
                yield x

    def read_json(path):
        with open(path,'r') as f:
            txt_raw = json.load(f)
        txt_raw = txt_raw['text']
        if isinstance(txt_raw, dict):
            txt_raw = list(txt_raw.values())
        return txt_raw

    def clean_txt(txt_raw):    
        txt_raw = list(flatten(txt_raw))
        txt_raw = ' '.join(txt_raw)

        # remove citations i.e. text between parentheses
        txt1 = re.sub("[\(\[].*?[\)\]]", " ", txt_raw)
        
        # replace whitespaces by regular spaces
        txt1 =  re.sub(r'\s+', ' ', txt1)
        # replace punctuations by regular spaces
        txt1 =  re.sub(r',', ' ', txt1)
        txt1 =  re.sub(r'\.', ' ', txt1)
        
        # assert only aleph-bet
        txt2 = "".join(c for c in txt1 if c in permitted_characters) #TODO use regex and replace by space
        #remove double spaces
        txt3 =  re.sub(' +', ' ', txt2)
        return txt3

    paths = {}
    main_path = 'data/tanchuma_text/' if os.path.exists("data") else '../data/tanchuma_text/'
    paths['Tanchuma'] = main_path+'Tsel Midrash Tanchuma.json'
    paths['Tanchuma Buber'] = main_path+'Midrash Tanhuma haKadum veHaYashan, S. Buber, 1885.json'
    paths['Shemot Rabbah'] = main_path+'Daat Shemot Rabbah.json'
    paths['Bemidbar Rabbah'] = main_path+'Daat Bemidbar Rabbah.json' # only from parasha 15
    paths['Devarim Rabbah'] = main_path+'Daat Devarim Rabbah.json'
    paths['Psikta Rabati'] = main_path+'OYW.json' #parashot 1-13, 31-47

    train_data = [] #bad practice but works
    test_data = []

    def preprocess_all(path):
        data_json = read_json(path)
        data_json_train, data_json_test = train_test_split(data_json,
                                                        test_size=test_size, random_state=random_state)
        train_data.append(clean_txt(data_json_train))
        test_data.append(clean_txt(data_json_test))

    preprocess_all(paths['Tanchuma'])
    preprocess_all(paths['Tanchuma Buber'])
    preprocess_all(paths['Shemot Rabbah'])
    preprocess_all(paths['Devarim Rabbah'])

    # last ones need special treatment because only part of the data is relevant

    bemidbar_json = read_json(paths['Bemidbar Rabbah'])
    bemidbar_json = bemidbar_json[14:]
    bemidbar_json_train, bemidbar_json_test = train_test_split(bemidbar_json,
                                                        test_size=test_size, random_state=random_state)
    train_data.append(clean_txt(bemidbar_json_train))
    test_data.append(clean_txt(bemidbar_json_test))


    psikta_json = read_json(paths['Psikta Rabati'])
    psikta_json = psikta_json[0:13] + psikta_json[30:]
    psikta_json_train, psikta_json_test = train_test_split(psikta_json,
                                                        test_size=test_size, random_state=random_state)
    train_data.append(clean_txt(psikta_json_train))
    test_data.append(clean_txt(psikta_json_test))

    return train_data, test_data