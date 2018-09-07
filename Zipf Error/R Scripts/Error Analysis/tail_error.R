# ANALYSIS THE ERROR STRUCTURE IN THE TAIL
# IE EG ERROR DISTRIBUTIONS BY FREQUENCY
library(ggplot2)
source("mandelbrot_mle.R")
source("mandelbrot_error.R")

lang <- "NO"

wiki.results <- wiki_mle(lang)
dat <- wiki.results$dats$Article
mle.result <- wiki.results$results$Article

error_dat <- mandelbrot_error(list(dat), list(mle.result))[[1]]
error_dat$count <- dat$count
plot_mandelbrot_error(error_dat, name=lang)


ggplot(error_dat[error_dat$count < 30, ]) + 
  geom_hex(aes(x=log(rank), y=log.diff.prob, colour=as.factor(count)), 
           bins=50)

ggplot(error_dat[error_dat$count < 10, ]) + 
  geom_freqpoly(aes(log.diff.prob, color=as.factor(count)), 
                binwidth=0.02)
ggplot(error_dat[error_dat$count < 15 & error_dat$count > 3,  ]) + 
  geom_density(aes(log.diff.prob, color=as.factor(count)))



count_err_dist <- lapply(sort(unique(error_dat$count)), 
                function(f){error_dat[error_dat$count == f, 5]})

names(count_err_dist) <- sort(unique(error_dat$count))
# plot(f, err(f)) where err(f) = (e_min, e_mean, e_max)
c_errs <- data.frame(count=sort(unique(error_dat$count)), 
                     mins=sapply(count_err_dist, min),
                     means=sapply(count_err_dist, median),
                     maxs=sapply(count_err_dist, max),
                     vars=sapply(count_err_dist, var))
c_errs$vars[is.na(c_errs$vars)] <- -0

# plots the variance of err_dist(c) against the counts c
ggplot(c_errs) + geom_point(aes(x=log(count), y=vars)) + 
  scale_x_reverse()

# plots counts c against mean(err_dist(c))
# includes errorbars for min and max of err_dist(c)
# and a LOESS smooth line
# -> may be preferrable over plotting ranks r against err(r)
ggplot(c_errs, aes(x=log(count), y=means)) + 
  geom_point(size=0.2)+
  geom_errorbar(aes(ymin=mins, ymax=maxs), size=0.2) + 
  geom_smooth(method = "loess", span=0.1)+
  scale_x_reverse() + 
  coord_cartesian(ylim = c(-1, 1))


# distribution over frequencies (prior on word-frequency dist)
h <- hist(log(unique(error_dat$count)), breaks = 300)








