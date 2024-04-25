# gum-signaling-analysis
Analysis of signaling annotations in GUM by relation and genre

## get data
Clone the data repository (should be in same directory as this project's directory, not inside this project's directory):

```
git clone https://github.com/amir-zeldes/gum/tree/master
```
Fill in tokens for reddit files (script included in GUM data repository):
```
python get_text.py
```

## extract singaling annotations
```
python extract_signal_annotations.py
```
Produces tsv file of signaling annotations.
Columns: DOC\_NAME, GENRE, COARSE\_RELATION, RELATION, SIGNAL\_TYPE,	SIGNAL\_SUBTYPE, TOKEN\_IDS

## variation analysis and visualization
```
python visualizations.py
```
Code for proportion visualizations.
```
python relation_variation.py
```
Code for inter-genre variation ranking and genre similarity dendrograms.
```
stats_data_analysis.R
```
Code for chi-squared tests and association plots.

## Surprisal Experiments
Please change the file path to the corresponding path for either causality data or explanation data (they are in the ```data_surprisal``` folder) and then run ```surprisal.ipynb```.