import matplotlib.pyplot as plt
from PIL import Image
from fastai.vision.all import *
from os import listdir
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from mlxtend.plotting import plot_confusion_matrix


#get predictions for a specific filder
def get_predictions(learn_object, TEST_FOLDER):
    return list(map(lambda x: (x, learn_object.predict(f"{TEST_FOLDER}/{x}")[0]), listdir(TEST_FOLDER)))

def show_predictions(learn_loaded, TEST_FOLDER):
    preds = get_predictions(learn_loaded, TEST_FOLDER)

    rows=5
    cols = 3
    img_count = 0

    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(20,20))

    for i in range(rows):
        for j in range(cols):        
            if img_count < len(preds):
                image=Image.open(f"{TEST_FOLDER}/{preds[img_count][0]}")
                axes[i, j].set_title(preds[img_count][1].split('_')[0])
                axes[i, j].imshow(image)
                img_count+=1
    fig.show()

def print_results(dir_classes, learn_loaded, DATASET_DIR, result_file):
    preds = []
    actuals = []
    for c in dir_classes:
        predictions = get_predictions(learn_loaded, f"{DATASET_DIR}/{c}")
        preds.extend(predictions)
        actuals.extend(np.full((1,len(predictions)), c).ravel().tolist())
    pred_vals = list(map(lambda x : x[1], preds))
    print('Accuracy', accuracy_score(actuals, pred_vals))
    print('F1 score', f1_score(actuals, pred_vals, average='macro'))
    print(classification_report(y_pred=actuals, y_true=pred_vals))
    classes = list(map(lambda x: x.split('_')[0],dir_classes))

    cm  = confusion_matrix(actuals, pred_vals)

    fig, ax = plot_confusion_matrix(conf_mat=cm, class_names=classes)
    plt.show()
    fig.savefig(result_file) 
    plt.close(fig)