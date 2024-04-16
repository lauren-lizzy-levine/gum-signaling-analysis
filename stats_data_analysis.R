data <-read.table(file.choose(), header=TRUE,stringsAsFactors=FALSE, sep="\t", fill = TRUE, quote = "") # choose file GUM_signals.tsv
data$SIGNAL_TYPE <- ifelse(data$SIGNAL_TYPE %in% c('orp'), 'dm', data$SIGNAL_TYPE)

# Remember: chi-squared is technically invalid if any if the cells in the contingency table are zeros


genre_collapse_data <- data
genre_collapse_data$GENRE <- ifelse(genre_collapse_data$GENRE %in% c("court", "interview", "podcast", "speech", "conversation", "vlog"), 'spoken', 'written')
genre_collapse_signal_type <- table(genre_collapse_data$SIGNAL_TYPE, genre_collapse_data$GENRE)
chisq.test(genre_collapse_signal_type)
assocplot(genre_collapse_signal_type)


signal_collapse_data <- data
signal_collapse_data$SIGNAL_TYPE <- ifelse(signal_collapse_data$SIGNAL_TYPE %in% c('dm'), 'explicit', 'implicit')

signal_collapse_genre <- table(signal_collapse_data$GENRE, signal_collapse_data$SIGNAL_TYPE)
chisq.test(signal_collapse_genre)
assocplot(signal_collapse_genre)

signal_collapse_relation <- table(signal_collapse_data$COARSE_RELATION, signal_collapse_data$SIGNAL_TYPE)
chisq.test(signal_collapse_relation)
assocplot(signal_collapse_relation)
