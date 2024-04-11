import pandas as pd
import matplotlib.pyplot as plt


def signal_proportion_by_relation(datafile, genre_list, genre_group_name, outfile):
	df = pd.read_csv(datafile, sep="\t")
	# Filter to have only genres in genre_list
	df = df[df['GENRE'].isin(genre_list)]
	# Add constant value for each row to count the occurrences
	df['Value'] = 1
	# Calculate proportions
	df['Total'] = df.groupby('COARSE_RELATION')['Value'].transform('sum')
	df['Proportion'] = df['Value'] / df['Total']
	# Pivot the DataFrame for plotting
	pivot_df = df.pivot_table(index='COARSE_RELATION', columns='SIGNAL_TYPE', values='Proportion', aggfunc='sum')
	#print(pivot_df)
	# Plot
	pivot_df.plot(kind='bar', stacked=True)
	plt.xlabel('Coarse Relation')
	plt.ylabel('Proportion')
	plt.title('Proportion of Signal Type to Coarse Relation for GUM ' + genre_group_name)
	plt.legend(title='Signal Type', bbox_to_anchor=(1, 1))
	plt.xticks(rotation=45)
	plt.savefig('visualizations/' + outfile, bbox_inches='tight')  # Save the plot as a PNG file with tight bounding box
	#plt.show()

	return

def create_signal_proportion_graphs():
	datafile = "GUM_signals.tsv"
	signal_proportion_by_relation(datafile, ["academic"], "Academic Writing", "academic_relation_signal.png")
	signal_proportion_by_relation(datafile, ["bio"], "Biographies", "bio_relation_signal.png")
	signal_proportion_by_relation(datafile, ["court"], "Courtroom Transcripts", "court_relation_signal.png")
	signal_proportion_by_relation(datafile, ["essay"], "Essays", "essay_relation_signal.png")
	signal_proportion_by_relation(datafile, ["fiction"], "Fiction", "fiction_relation_signal.png")
	signal_proportion_by_relation(datafile, ["whow"], "How-to Guides", "whow_relation_signal.png")
	signal_proportion_by_relation(datafile, ["interview"], "Interviews", "interview_relation_signal.png")
	signal_proportion_by_relation(datafile, ["letter"], "Letters", "letter_relation_signal.png")
	signal_proportion_by_relation(datafile, ["news"], "News", "news_relation_signal.png")
	signal_proportion_by_relation(datafile, ["reddit"], "Reddit", "reddit_relation_signal.png")
	signal_proportion_by_relation(datafile, ["podcast"], "Podcasts", "podcast_relation_signal.png")
	signal_proportion_by_relation(datafile, ["speech"], "Political Speeches", "speech_relation_signal.png")
	signal_proportion_by_relation(datafile, ["conversation"], "Conversations", "conversation_relation_signal.png")
	signal_proportion_by_relation(datafile, ["textbook"], "Textbooks", "textbook_relation_signal.png")
	signal_proportion_by_relation(datafile, ["voyage"], "Travel Guides", "voyage_relation_signal.png")
	signal_proportion_by_relation(datafile, ["vlog"], "Vlogs", "vlog_relation_signal.png")
	written_genres = ["academic", "bio", "essay", "fiction", "whow", "letter", "news", "reddit", "textbook", "voyage"]
	spoken_genres = ["court", "interview", "podcast", "speech", "conversation", "vlog"]
	signal_proportion_by_relation(datafile, written_genres, "Written", "written_relation_signal.png")
	signal_proportion_by_relation(datafile, spoken_genres, "Spoken", "spoken_relation_signal.png")
	return

if __name__ == "__main__":
	create_signal_proportion_graphs()