# obtaining and plotting error of MLE on Mandelbrot
library(stats4)
library(randtests)
library(ggplot2)
library(hexbin)
library(qqplotr)
# loads mandel.pdf and mandel.norm
source("probability_definitions.R")
source("util_functions.R")
source("mandelbrot_mle.R")
source("mandelbrot_error.R")

mandelbrot_samples <- function(word_set, alpha, beta, N){
  mandel_probs <- mandel.pdf(alpha, beta, word_inds)
  words <- sample(word_inds, size = N, replace = TRUE, prob = mandel_probs)
  count_frame <- as.data.frame(table(words))
  words <- sample(word_inds, size = N, replace = TRUE, prob = mandel_probs)
  rank_frame <- as.data.frame(table(words))
  intersected_frames <- unified_df_intersect(list(rank_frame, count_frame), 
                                             var_to_intersect = "words")
  samples <- intersected_frames[[1]]
  samples <- samples[order(samples$Freq, decreasing = TRUE), ]
  samples$rank <- c(1:dim(samples)[1])
  samples <- samples[order(samples$words), ]
  samples$count <- intersected_frames[[2]]$Freq
  samples <- samples[order(samples$rank), ]
  return(samples)
}


# SAMPLE GENERATION
# (use empirical parameters for comparison with empirical distributions)
alpha <- 1
beta <- 2
word_inds <- c(1:100000)
N <- 20000000
samples <- mandelbrot_samples(word_inds, alpha, beta, N)

# MLE
mle.result <- mandelbrot_mle(list(random_samples = samples))
last_plot() + geom_smooth(aes(rank, count), span = 0.05)

# ERROR ANALYSIS
error.dat <- mandelbrot_error(list(random_samples = samples), mle.result)
last_plot() + geom_smooth(aes(log(rank), log.diff.prob))# , method = 'loess')
error.dat <- error.dat$random_samples

# significant -> nonrandom
runs.test(error.dat$log.diff.prob, plot = T)
# p = 0.009 -> nonrandom
turning.point.test(error.dat$log.diff.prob)
# significant -> nonrandom
bartels.rank.test(error.dat$log.diff.prob)
# p = 0.007 -> nonrandom
cox.stuart.test(error.dat$log.diff.prob)
# p = 0.32 -> random
difference.sign.test(error.dat$log.diff.prob)
# significant -> trand, i.e. nonrandom
rank.test(error.dat$log.diff.prob)


sizes <- seq(100, 7000, by=50)
sign_tests <- sapply(sizes, 
                     function(s){turning.point.test(
                       error.dat$log.diff.prob[1:s])})
names(sign_tests) <- sizes

ggplot() + geom_point(aes(sizes, 
                          sapply(sign_tests, `[[`, "statistic"),
                          colour=sapply(sign_tests, `[[`, "p.value"))) + 
  geom_smooth(aes(sizes, sign_tests), span=0.5)


mean(error.dat$log.diff.prob)
# distribution of error 
# -> more mass to the right of the mean because of tail
ggplot(error.dat) + geom_histogram(aes(log.diff.prob), 
                                   binwidth = 0.01)
# empirical cdfs of basline distribution and a normal with same params
# -> similar with slight divergences
ggplot(error.dat) + stat_ecdf(aes(log.diff.prob), geom="step") + 
  stat_ecdf(aes(rnorm(50000, mean=0.002705753, sd=0.09563566)), 
            geom="step", colour="red")

# TESTS (reject H_0 if p<\alpha)
# K-S Test (two-sided): H_0 := emp. prob. is equal to hypothetical prob.
# -> difference between empirical and normal significant
ks.test(error.dat$log.diff.prob, "pnorm", 
        mean=0.002705753, sd=0.09563566)

# L-B Test: H_0 := no serial correlation 
#   (randomness in the sense of correlation)
# -> autocorrelation found
Box.test(error.dat$log.diff.prob, type="Ljung-Box")


# plot Ljung-Box statistics for various sizes (starting from the front)
sizes <- seq(10, length(word_inds), by=50)
test_vals <- lapply(sizes,
                    function(s) Box.test(error.dat$log.diff.prob[1:s], 
                                         lag = 1,  type = "Ljung-Box"))
names(test_vals) <- sizes
ggplot() + geom_point(aes(x=sizes,
                          y=sapply(test_vals, `[[`, "statistic"),
                          colour=sapply(test_vals, `[[`, "p.value") < 0.01),
                      show.legend = FALSE)


# ANAlYSE THE ERROR GROUPED INTO DISTRIBUTIONS BY FREQUENCY
# -> means of distributions still autocorrelated
error.dat$count <- samples$count
c_err_dst <- count_err_dist(error.dat)
Box.test(sapply(c_err_dst, median), type = "Ljung-Box")
Box.test(unlist(c_err_dst), type = "Ljung-Box")