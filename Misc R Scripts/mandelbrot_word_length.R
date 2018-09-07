# PLOT CORRELATION BETWEEN ZIPF'S LAW AND WORD LENGTH
library(ggplot2)
library(stringdist)
source("util_functions.R")

f <- "../Estimates/FI_ToktokTokenizer_ArticleSplitter"
dat <- load_wiki_dat(single_file_name = f)

ggplot(dat) + geom_hex(aes(rank, count), bins=75) + scale_y_log10() + scale_x_log10()


dat$len <- nchar(as.character(dat$word))

ggplot(dat) + geom_point(aes(x=rank, y=count, colour=1/len)) + 
  scale_y_log10() + scale_x_log10()


for (l in sort(unique(dat$len))){
  len_dat <- dat[dat$len==l, ]
  if(nrow(len_dat) > 1000){
    p <- ggplot(len_dat) + 
          geom_hex(aes(x=rank, y=count), bins=50) + 
          scale_y_log10() + scale_x_log10() + 
          labs(title = paste("length:", l, 
                             "(", nrow(len_dat), "words)"))
    print(p)
  }
}
