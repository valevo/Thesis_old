# TESTS FOR AUTOCORRELATION 
library(ggplot2)
library(stats)
source("mandelbrot_mle.R")
source("mandelbrot_error.R")

lang <- "VI"

# load data and MLE
wiki.results <- wiki_mle(lang)
dat <- wiki.results$dats$Article
mle.result <- wiki.results$results$Article

# get error from MLE
error_dat <- mandelbrot_error(list(dat), list(mle.result))[[1]]
plot_mandelbrot_error(error_dat, lang)
error_dat$count <- dat$count

acf_val <- acf(error_dat$log.diff.prob)

# apply Box-Ljung test to subsections (increasing size)
# starting from lowest ranks
sizes <- seq(100, 200000, by=100)
test_vals <- lapply(sizes,
                     function(s) Box.test(error_dat$log.diff.prob[1:s], 
                                         lag = 1,  type = "Ljung-Box"))
names(test_vals) <- sizes
# log-transform of x-axis emphasises low sizes
# -> more informative
# maximum is at subset 1:6600 (excluding the 'scoop' in the tail)
ggplot() + geom_point(aes(log(sizes, 10),
                          sapply(test_vals, `[[`, "statistic")))


# tests autocorrelation by creating two lagged copies of the data
lagged <- function(l, v){ list(v1 = head(v, -l), v2 = tail(v, -l))}
lag_cor <- function(l, v){cor.test(lagged(l, v)$v1, lagged(l, v)$v2)}
cors <- lapply(seq(1, 10000, by=50), 
               function(l) lag_cor(l, error_dat$log.diff.prob))
names(cors) <- seq(1, 10000, by=50)
ggplot() + geom_point(aes(seq(1, 10000, by=50),
                          sapply(cors, `[[`, "estimate")), size=0.5)

which.max(sapply(cors, `[[`, "estimate"))


vs <- lagged(101, error_dat$log.diff.prob[1:200000])
cor.test(vs$v1, vs$v2)

ggplot() + geom_hex(aes(x=vs$v1, y=vs$v2), bins = 100)

l <- 101  # maximal correlation at lag 5
lag_df <- data.frame(lagged(l, error_dat$log.diff.prob), 
                     c=head(error_dat$rank, -l))
cor.test(lag_df$v1, lag_df$v2)
ggplot(lag_df, aes(x=log(c))) + 
  geom_hex(aes(y=v1+2), bins=200, colour="blue") + 
  geom_hex(aes(y=v2-2), bins=200, colour="red")




# using count-error distributions and means as surrogates
c_e_dist <- count_err_dist(error_dat)
err_means <- sapply(c_e_dist, mean)




Box.test(error_dat$log.diff.prob)
lapply(c(1:10), function(l) Box.test(err_means, lag=l))


ggplot(error_dat[1:100000, ], aes(log(rank), log.diff.prob)) + 
  geom_point(aes(color=log.diff.prob > 0), size=0.1)

ggplot() + geom_point(aes(log(sort(unique(error_dat$count))), 
                          sapply(c_e_dist, mean),
                          colour=sapply(c_e_dist, mean) > 0), 
                      size=0.1, show.legend = F) + 
  scale_x_reverse()  


ggplot(error_dat) + geom_histogram(aes(log.diff.prob), binwidth = 0.05)
