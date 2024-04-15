from scipy.spatial import distance
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')


def frequency_counts_coarserel_genre(infile):
	lines = []
	with open(infile, "r") as file:
		reader = csv.reader(file, delimiter='\t')
		next(reader, None)  # skip the headers
		for line in reader:
			lines.append(line)
	freq_counts = {}
	for line in lines:
		genre = line[1]
		coarse_relation = line[2]
		signal_type = line[4]
		if signal_type == 'orp':
			signal_type = 'dm'
		if coarse_relation in freq_counts:
			if genre in freq_counts[coarse_relation]:
				if signal_type in freq_counts[coarse_relation][genre]:
					freq_counts[coarse_relation][genre][signal_type] += 1
				else:
					freq_counts[coarse_relation][genre][signal_type] = 1
			else:
				freq_counts[coarse_relation][genre] = {signal_type: 1}
		else:
			freq_counts[coarse_relation] = {genre: {signal_type: 1}}

	# fill in zeros
	singal_types = ['dm', 'grf', 'lex', 'mrf', 'num', 'ref', 'sem', 'syn']
	for coarse_relation in freq_counts:
		for genre in freq_counts[coarse_relation]:
			for sig_type in singal_types:
				if sig_type not in freq_counts[coarse_relation][genre]:
					freq_counts[coarse_relation][genre][sig_type] = 0

	return freq_counts

def pairwise_jsd(freq_counts):
	pair_distances = {}
	singal_types = ['dm', 'grf', 'lex', 'mrf', 'num', 'ref', 'sem', 'syn']
	for coarse_relation in freq_counts:
		pair_distances[coarse_relation] = {}
		genre_pairs_seen = set()
		for genre1 in freq_counts[coarse_relation]:
			for genre2 in freq_counts[coarse_relation]:
				if (genre2, genre1) not in genre_pairs_seen and genre1 != genre2:
					genre1_counts = []
					genre2_counts = []
					for sig in singal_types:
						genre1_counts.append(freq_counts[coarse_relation][genre1][sig])
						genre2_counts.append(freq_counts[coarse_relation][genre2][sig])
					pair_distances[coarse_relation][(genre2, genre1)] = distance.jensenshannon(genre1_counts, genre2_counts)
					genre_pairs_seen.add((genre2, genre1))
					genre_pairs_seen.add((genre1, genre2))

	return pair_distances

def rank_variation(pair_distances):
	# Which relations show the most inter-genre variation?
	# For each relation, calculate pair-wise avg of JSD, then sort in decending order
	relation_avg_jsd = []
	for relation in pair_distances:
		pairs_count = len(pair_distances[relation])
		jsd_sum = 0
		for pair in pair_distances[relation]:
			jsd_sum += pair_distances[relation][pair]
		relation_avg_jsd.append((relation, jsd_sum / pairs_count))
	relation_jsd_sorted_descending = sorted(relation_avg_jsd, key=lambda x: x[1], reverse=True)
	for rel_jsd in relation_jsd_sorted_descending:
		print(rel_jsd)
		#('organization', 0.3575705520997728)
		#('explanation', 0.34831146431631826)
		#('restatement', 0.2965876654702925)
		#('context', 0.2741118748162802)
		#('joint', 0.2352734773629788)
		#('mode', 0.19919851956411835)
		#('causal', 0.19592911381159392)
		#('contingency', 0.18613163957265172)
		#('elaboration', 0.17102395611252416)
		#('purpose', 0.11921745935527214)
		#('attribution', 0.11417348527138776)
		#('adversative', 0.08437153764023812)
		#('evaluation', 0.02908569613791581)
	# Make visualizaions

	return

def make_distance_matrix(distances):
	genres = ["academic", "bio", "conversation", "court", "essay", "fiction", "interview", 
	"letter", "news", "podcast", "reddit", "speech", "textbook", "vlog", "voyage", "whow"]
	distance_matrix = []
	for genre1 in genres:
		row = []
		for genre2 in genres:
			if genre1 == genre2:
				row.append(0)
			elif (genre1, genre2) in distances:
				row.append(distances[(genre1, genre2)])
			elif (genre2, genre1) in distances:
				row.append(distances[(genre2, genre1)])
			else:
				print("DANGER")
		distance_matrix.append(row)

	return np.array(distance_matrix), genres


def make_dendrogram(relation, pair_distances):
	# Will illustrate which genres signal the gives relation most similarly/differently
	# Make distance matrix
	distance_matrix, genres = make_distance_matrix(pair_distances[relation])
	dists = squareform(distance_matrix)
	linkage_matrix = linkage(dists, "average")
	# Make visualizaion
	dendrogram(linkage_matrix, labels=genres)
	plt.title('Signaling similarity between genres for relation: ' + relation)
	plt.xticks(rotation=45)
	plt.show()
	return

def coarse_level_variation():
	datafile = "GUM_signals.tsv"
	freq_counts = frequency_counts_coarserel_genre(datafile)
	pair_distances = pairwise_jsd(freq_counts)
	#rank_variation(pair_distances)
	make_dendrogram("restatement", pair_distances)
	#print(freq_counts)


if __name__ == "__main__":
	coarse_level_variation()