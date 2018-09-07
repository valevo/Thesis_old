# ANALYSE THE VERSION OF ZIPF IN WHICH
#   V(m) \propto 1/m
library(ggplot2)
source("util_functions.R")


f <- "../Estimates/FI_ToktokTokenizer_ArticleSplitter"

dat <- load_wiki_dat(single_file_name = f)


# count the frequencies loaded from the Wikipedia frequency table:
# V(m) = |{w \in V s.t. freq(w) = m}|
v_m <- as.data.frame(table(dat$count))
names(v_m) <- c("m", "count")
v_m$m <- as.numeric(levels(v_m$m))


# plot each frequency against the number of words wth that frequency
ggplot(v_m) + geom_point(aes(m, count)) + 
  scale_y_log10() + scale_x_log10()


# same plot as above but with bars
ggplot(v_m) + geom_col(aes(m, count)) + 
  coord_cartesian(xlim = c(0,250), ylim = c(0, 50000)) #+ scale_y_log10()# + scale_x_log10()


# establish and plot the distribution over V(m), i.e.
# the frequency of each V(m) (e.g. many m s.t. V(m) = 1)
lengths <- sapply(sort(unique(v_m$count)), 
                  function(c){nrow(v_m[v_m$count == c, ])})
ggplot() + geom_point(aes(sort(unique(v_m$count)), lengths)) + 
  scale_y_log10() + scale_x_log10()
                                                                                                                                                                                                    
