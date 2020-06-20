from csv import reader
from random import seed
from random import randrange
def accuracyfinder(expected, got):
	correct = 0
	for i in range(len(expected)):
		if expected[i] == got[i]:
			correct += 1
	return correct / float(len(expected)) * 100.0
def kfold_crossvalidation_split(dataset, n_folds):
	splitting_dataset = list()
	copyingdataset = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(copyingdataset))
			fold.append(copyingdataset.pop(index))
		splitting_dataset.append(fold)
	return splitting_dataset
def readingfilecsv(filename):
	file = open(filename, "rt")
	lines = reader(file)
	dataset = list(lines)
	return dataset
def columnfloatstr(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())
def model(dataset, algorithm, n_folds, *args):
	folds = kfold_crossvalidation_split(dataset, n_folds)
	scores = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
		got = algorithm(train_set, test_set, *args)
		expected = [row[-1] for row in fold]
		accuracy = accuracyfinder(expected, got)
		scores.append(accuracy)
	return scores
def gini_index(groups, classes):
	n_instances = float(sum([len(group) for group in groups]))
	gini = 0.0
	for group in groups:
		size = float(len(group))
		if size == 0:
			continue
		score = 0.0
		for class_val in classes:
			p = [row[-1] for row in group].count(class_val) / size
			score += p * p
		gini += (1.0 - score) * (size / n_instances)
	return gini
def get_split(dataset):
	class_values = list(set(row[-1] for row in dataset))
	b_index, b_value, b_score, b_groups = 999, 999, 999, None
	for index in range(len(dataset[0])-1):
		for row in dataset:
			groups = splittingtestingsets(index, row[index], dataset)
			gini = gini_index(groups, class_values)
			if gini < b_score:
				b_index, b_value, b_score, b_groups = index, row[index], gini, groups
	return {'index':b_index, 'value':b_value, 'groups':b_groups}
def to_terminal(group):
	outcomes = [row[-1] for row in group]
	return max(set(outcomes), key=outcomes.count)
def splittingtestingsets(index, value, dataset):
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right
def split(node, max_depth, min_size, depth):
	left, right = node['groups']
	del(node['groups'])
	if not left or not right:
		node['left'] = node['right'] = to_terminal(left + right)
		return
	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return
	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		node['left'] = get_split(left)
		split(node['left'], max_depth, min_size, depth+1)
	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		node['right'] = get_split(right)
		split(node['right'], max_depth, min_size, depth+1)
def build_tree(train, max_depth, min_size):
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root
def decision_tree(train, test, max_depth, min_size):
    tree = build_tree(train, max_depth, min_size)
    print_tree(tree)
    predictions = list()
    for row in test:
        prediction = predict(tree, row)
        predictions.append(prediction)
    return(predictions)
def print_tree(node, depth=0):
	if isinstance(node, dict):
		print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
		print_tree(node['left'], depth+1)
		print_tree(node['right'], depth+1)
	else:
		print('%s[%s]' % ((depth*' ', node)))
def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']
seed(1)
def pgen(max_depth):
    filename = 'data_banknote_authentication.csv'
    dataset = readingfilecsv(filename)

    for i in range(len(dataset[0])):
       columnfloatstr(dataset, i)
        # evaluate algorithm
    n_folds = 5
    min_size = 10
    scores = model(dataset, decision_tree, n_folds, max_depth, min_size)
    print('Scores: %s' % scores)
    print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))
    return (sum(scores)/float(len(scores)))
dd=1
flag=0
while(flag==0):
    val_orig=pgen(dd)
    val_new=pgen(dd+1)

    if(val_new<val_orig):
        print("Final depth:",dd)
        flag=1
    else:
        dd+=1
