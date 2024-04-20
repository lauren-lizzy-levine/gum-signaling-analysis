from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')

def frequency_counts_rel_sig(infile, coarse=False):
	lines = []
	with open(infile, "r") as file:
		reader = csv.reader(file, delimiter='\t')
		next(reader, None)  # skip the headers
		for line in reader:
			lines.append(line)
	freq_counts = {}
	for line in lines:
		if coarse:
			relation = line[2] # coarse relation
		else:
			relation = line[3]
		signal_type = line[4]
		if signal_type == 'orp':
			signal_type = 'dm'
		if relation in freq_counts:
			if signal_type in freq_counts[relation]:
				freq_counts[relation][signal_type] += 1
			else:
				freq_counts[relation][signal_type] = 1
		else:
			freq_counts[relation] = {signal_type: 1}

	# fill in zeros
	singal_types = ['dm', 'grf', 'lex', 'mrf', 'num', 'ref', 'sem', 'syn']
	for relation in freq_counts:
		for sig_type in singal_types:
			if sig_type not in freq_counts[relation]:
				freq_counts[relation][sig_type] = 0

	# eliminate topic-solutionhood because it only occura 8 times
	if "topic-solutionhood" in freq_counts:
		freq_counts.pop("topic-solutionhood")

	return freq_counts

def pairwise_jsd(freq_counts):
	pair_distances = {}
	singal_types = ['dm', 'grf', 'lex', 'mrf', 'num', 'ref', 'sem', 'syn']
	relation_pairs_seen = set()
	for relation1 in freq_counts:
		for relation2 in freq_counts:
			if (relation2, relation1) not in relation_pairs_seen and relation1 != relation2:
				relation1_counts = []
				relation2_counts = []
				for sig in singal_types:
					relation1_counts.append(freq_counts[relation1][sig])
					relation2_counts.append(freq_counts[relation2][sig])
				pair_distances[(relation2, relation1)] = distance.jensenshannon(relation1_counts, relation2_counts)
				relation_pairs_seen.add((relation2, relation1))
				relation_pairs_seen.add((relation1, relation2))

	#print(pair_distances)
	#pair_distances_sorted_descending = sorted(pair_distances, key=lambda x: x[1], reverse=True)

	return pair_distances

def make_distance_matrix(distances):
	relations = sorted(list(set([x[0] for x in distances.keys()] + [x[1] for x in distances.keys()])))

	distance_matrix = []
	for relation1 in relations:
		row = []
		for relation2 in relations:
			if relation1 == relation2:
				row.append(0)
			elif (relation1, relation2) in distances:
				row.append(distances[(relation1, relation2)])
			elif (relation2, relation1) in distances:
				row.append(distances[(relation2, relation1)])
			else:
				print("DANGER")
		distance_matrix.append(row)

	return np.array(distance_matrix), relations

def sort_relation_pairs(pair_score):
	score_list = [(x, pair_score[x]) for x in pair_score]
	sorted_pair_list = sorted(score_list, key=lambda x: x[1])
	# write to file
	with open('relation_pairs.txt', 'w') as f:
		for pair in sorted_pair_list:
			f.write(f"{pair}\n")
	return


if __name__ == "__main__":
	datafile = "GUM_signals.tsv"
	freq_counts = frequency_counts_rel_sig(datafile, coarse=True)
	pair_distances = pairwise_jsd(freq_counts)
	sort_relation_pairs(pair_distances)
	distance_matrix, relations = make_distance_matrix(pair_distances)
	ax = sns.heatmap(distance_matrix, vmin=0, vmax=1, xticklabels=relations, yticklabels=relations, annot=True)
	plt.tight_layout()
	plt.savefig('visualizations/' + "relation_heatmap.png")
	#plt.show()
