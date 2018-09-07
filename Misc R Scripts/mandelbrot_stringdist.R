library(ggplot2)
library(stringdist)
source("util_functions.R")


f <- "../Estimates/ALS_ToktokTokenizer_ArticleSplitter"

dat <- load_wiki_dat(single_file_name = f)
dat$word <- as.character(dat$word)



length_filter <- function(l, ls){ls[abs(l-nchar(ls)) <= l/2]}
filtered <- lapply(sort(unique(nchar(dat$word))), 
                   function(l) length_filter(l, dat$word))
names(filtered) <- sort(unique(nchar(dat$word)))

filtered_distances <- function(w){
  l <- nchar(w)
  stringdist(w, filtered[[as.character(l)]])
}
n <- 100
distances <- lapply(dat$word[1:n], filtered_distances)
names(distances) <- dat$word[1:n]

norm <- function(v) {v/max(v)}

normed_distances <- lapply(distances, norm)
normed_distances <- lapply(normed_distances, function(ds){
  Filter(function(d){d < 0.3}, ds)})

ggplot() + geom_point(aes(x=log(dat$count[1:n]), 
                          y=sapply(normed_distances, mean)))

