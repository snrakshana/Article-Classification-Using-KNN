import os
from utils import open_file, read_files, open_files, write_classified_to_path
from utils.classifier.KNNClassifier import KNNClassifer

if __name__ == '__main__':
    # read positive and negative words
    positive_words = open_file('./positive_words.txt')
    negative_words = open_file('./negative_words.txt')

    x_train = [positive_words, negative_words]
    y_train = [0, 1]

    # read and open saved lowercase articles
    files = read_files('./output/clean')
    adaderana_data, dailymirror_data, hirunews_data, newsfirst_data, sundaytimes_data = open_files(files)

    # fit training data on KNN model
    knn = KNNClassifer(k=1, distance_type='path')
    knn.fit(x_train, y_train)

    # predict for adaderana data
    adaderana_pred = knn.predict(adaderana_data)
    write_classified_to_path('./output/classified/adaderana', adaderana_data, adaderana_pred)

    # predict for dailymirror data
    dailymirror_pred = knn.predict(dailymirror_data)
    write_classified_to_path('./output/classified/dailymirror', dailymirror_data, dailymirror_pred)

     #predict for hirunews data
    hirunews_pred = knn.predict(hirunews_data)
    write_classified_to_path('./output/classified/hirunews', hirunews_data, hirunews_pred)

    # predict for newsfirst data
    newsfirst_pred = knn.predict(newsfirst_data)
    write_classified_to_path('./output/classified/newsfirst', newsfirst_data, newsfirst_pred)

    # predict for sudaytimes data
    sundaytimes_pred = knn.predict(sundaytimes_data)
    write_classified_to_path('./output/classified/sundaytimes', sundaytimes_data, sundaytimes_pred)

