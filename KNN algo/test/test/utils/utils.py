import os
import io

def read_files(dir):
    """
    Read all the files in a given directory and return a list of file paths.
    Args:
        dir: path to file directory

    Returns:
        list of file paths
    """
    print('[INFO] Reading data...')
    f = []
    for roots, dirs, files in os.walk(dir):
        for file in files:
            f.append(os.path.join(roots, file))
    return f

def open_file(file_path):
    """
    Open the file in the given directory and return a list of the content in the doc.
    Args:
        file_path: path to file directory

    Returns:
        list of the content in the doc
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        words = f.readlines()
    words = [word.strip() for word in words]
    return words

# open specific file paths
def open_files(file_paths):
    """
    Open the files in the given directory and return a list of docs.
    Args:
        file_paths: path to file directory

    Returns:
        list of the docs
    """
    adaderana = []
    dailymirror = []
    hirunews = []
    newsfirst = []
    sundaytimes = []
    
    for path in file_paths:
        if "adaderana" in path:
            w = open(path, encoding='utf-8', errors='ignore')
            adaderana += [w.read()]
        elif "dailymirror" in path:
            w = open(path, encoding='utf-8', errors='ignore')
            dailymirror += [w.read()]
        elif "hirunews" in path:
            w = open(path, encoding='utf-8', errors='ignore')
            hirunews += [w.read()]
        elif "newsfirst" in path:
            w = open(path, encoding='utf-8', errors='ignore')
            newsfirst += [w.read()]
        elif "sundaytimes" in path:
            w = open(path, encoding='utf-8', errors='ignore')
            sundaytimes += [w.read()]

    print('[INFO] {} files opened'.format(len(adaderana) + len(dailymirror) + len(hirunews) + len(newsfirst) + len(sundaytimes)))
    return adaderana, dailymirror, hirunews, newsfirst, sundaytimes


def to_lower_case(data_list):
    """
    Convert the text to lower case
    Args:
        data_list: list of text docs

    Returns:
        list of text docs
    """
    data_set = [" ".join(doc.split()).lower() for doc in data_list]
    print('[INFO] (lower case) -> Task Complete')
    return data_set

def remove_stopwords(data_list, stopwords):
    """
    Remove the stopwords in the given docs.
    Args:
        data_list: list of docs
        stopwords: list of stopwords

    Returns:
        list of docs
    """
    clean_data = []
    for doc in data_list:
        words = doc.split(' ')
        clean = [word for word in words if word not in stopwords]
        clean_data += [' '.join(clean)]
    print('[INFO] (remove stop words) -> Task Complete')
    return clean_data


def write_to_path(path, data_list):
    """
    Write given list of text docs into files
    Args:
        path: path to save directory
        data_list: list of text docs
    """
    i = 1
    if not os.path.exists(path):
        os.makedirs(path)
    for doc in data_list:
        f = open('{}/doc{}.txt'.format(path, i), 'w', encoding="utf-8")
        f.write(doc)
        f.close()
        i += 1
    print('[INFO] (write to path) -> Task Complete')

def write_classified_to_path(path, data_list, predict_list):
    """
    Write given list of news docs and their predicted news class into files
    Args:
        path: path to save directory
        data_list: list of text docs
        predict_list: predicted class list
    """
    i = 1
    if not os.path.exists(path):
        os.makedirs(path)
    for doc, pred in zip(data_list, predict_list):
        f = open('{}/doc{}.txt'.format(path, i), 'w', encoding="utf-8")
        f.write('News category: {} news\n'.format('Positive' if pred == 0 else 'Negative'))
        f.write('News content: {}'.format(doc))
        f.close()
        i += 1
    print('[INFO] (write to path) -> Task Complete')