from sklearn.metrics import classification_report
def cls_report_file(model_name, model, x_train, y_train, x_test, y_test):
    model.fit(x_train, y_train)
    prediction = model.predict(x_test)
    S = '\n {}: \n {} \n\n'.format(30*" "+model_name, classification_report(y_test, prediction))
    with open('results\cls_metrics.txt', 'a') as f:
        f.write(S)
    f.close()