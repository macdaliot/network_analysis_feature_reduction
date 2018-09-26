import numpy as np
from tabulate import tabulate
try:
    from classifiers import VisualClassifier
except ImportError:
    raise ImportError('Error importing! Add the root of the repository to your PYTHONPATH and try again.')


categories = ['attack_cat_Analysis', 'attack_cat_Backdoor', 'attack_cat_DoS',
              'attack_cat_Exploits', 'attack_cat_Fuzzers', 'attack_cat_Generic',
              'attack_cat_Reconnaissance', 'attack_cat_Shellcode', 'attack_cat_Worms',
              'label_0']
categories_short = ['Analysis', 'Backdoor', 'DoS',
                    'Exploits', 'Fuzzers', 'Generic',
                    'Reconnaissance', 'Shellcode', 'Worms',
                    'label_0']

visual_classifier = VisualClassifier(leafsize=1000)


def train_visual_classifier(df_train, cats_nr_train):
    visual_classifier.fit(df_train, cats_nr_train)


def get_attributes(source, df, radius_source, radius_slider,
                   point_info, point_probabilities):
    try:
        idx = source.selected._property_values['indices'][0]
    except KeyError:
        radius_source.data = {'x': [], 'y': [], 'rad': []}
        return
    dpoint = df.iloc[source.data['index'][idx]]

    # draw radius circle
    radius_source.data = {'x': [dpoint.x_cats_ae],
                          'y': [dpoint.y_cats_ae],
                          'rad': [radius_slider.value]}

    # update table with point info
    bin_class = {0: 'Normal', 1: 'Attack'}
    visual_pred = visual_classifier.predict(np.array([
        dpoint.x_cats_ae,
        dpoint.y_cats_ae
    ]), eps=radius_slider.value)
    visual_pred_str = ('✅ ' if visual_pred == dpoint.category else '❌ ') + \
        categories_short[visual_pred] if visual_pred != -1 else 'Unknown'

    cats_pred = ('✅ ' if dpoint.cats_ae_pred == (dpoint.category != 9) else '❌ ') + bin_class[dpoint.cats_ae_pred]
    orig_pred = ('✅ ' if dpoint.original_pred == (dpoint.category != 9) else '❌ ') + bin_class[dpoint.original_pred]
    point_info.text = '<div class="attrs">' + tabulate([
        ['category', categories_short[dpoint.category]],
        ['cats_ae_pred', cats_pred],
        ['original_pred', orig_pred],
        ['x', '{:.4f}'.format(dpoint.x_cats_ae)],
        ['y', '{:.4f}'.format(dpoint.y_cats_ae)],
        ['visual_pred', visual_pred_str],
    ], tablefmt='html') + '</div>'
    probs = visual_classifier.predict_proba(np.array([
        dpoint.x_cats_ae,
        dpoint.y_cats_ae
    ]), eps=radius_slider.value)
    point_probabilities.text = '<div class="probs">' + tabulate(
        [['{:.4f}'.format(x) for x in probs]],
        headers=categories_short,
        numalign='left',
        tablefmt='html') + '</div>'
