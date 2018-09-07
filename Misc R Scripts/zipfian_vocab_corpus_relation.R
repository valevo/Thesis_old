# EMPIRICALLY ASSESS CONSEQUENCES OF ZIPF FOR SAMPLING
# IE WHICH SHARES OF VOCABULARY CONSTITUTE WHICH SHARES OF THE CORPUS
library(ggplot2)
source("util_functions.R")

lang <- "ALS"
folder <- "../Estimates"

f <- "../Estimates/FI_ToktokTokenizer_ArticleSplitter"

dat <- load_wiki_dat(single_file_name = f)

ggplot(dat) + stat_ecdf(aes(count), pad = TRUE) + 
  geom_hline(yintercept = 0.5) + 
  scale_y_log10() + scale_x_log10()


less_than_x <- function(x) dat$count < x
x = 4

upper <- dat[!less_than_x(x), ]
lower <- dat[less_than_x(x), ]


dat$normed_c <- dat$count/sum(dat$count)
dat$cum_probs <- cumsum(dat$normed_c)

ggplot(dat) + geom_hex(aes(x = rank, y = cum_probs), bins=75) + 
  geom_hline(yintercept =  dat$cum_probs[1829], colour="red") + 
  geom_vline(xintercept =  1829, colour="red") + 
  scale_y_log10() + scale_x_log10()

ggplot(dat) + geom_hex(aes(x = rank, y = normed_c), bins=75) + 
  geom_hline(yintercept =  dat$normed_c[1829], colour="red") + 
  geom_vline(xintercept =  1829, colour="red") + 
  scale_y_log10() + scale_x_log10()


# 1829 is the FIRST rank s.t. sum(normed_counts)[1:r] > 0.5
# => 1829/length(counts) = 0.0019, i.e. the first 1828 types (or 0.2%)
#  make up half of the corpus
# =>  the vast majority of types (99.8%) make up only half the corpus
# => the probability of the type at rank 1829 is 0.00005, i.e.
#  half the corpus is made up of types with probability lower than 0.00005

ggplot(dat) + geom_hex(aes(x = rank, y = normed_c), bins=75) + 
  geom_hline(yintercept =  1/nrow(dat), colour="red") + 
  scale_y_log10() + scale_x_log10()

# 92% of all types have probability less than 10^-6 
#   (which would be roughly uniform)






