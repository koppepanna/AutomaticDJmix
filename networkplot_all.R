setwd("/Users/kosukefukui/djlog")
ml <- read.csv("music_list_all.csv")
ml
library(igraph)
ai.net <- graph.data.frame(ml,directed=F) 
# png(filename="setlist_all.png", width=2000, height=1600)
plot(ai.net, vertex.size = 5,vertex.label.cex = 1.8)
# dev.off()