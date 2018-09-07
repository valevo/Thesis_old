# TEST EMPIRICAL MANDELBROT ERROR DISTRIBUTION FOR NORMALITY
source("mandelbrot_mle.R")
source("mandelbrot_error.R")

lang <- "ID"
wiki.results <- wiki_mle(lang)
dats <- wiki.results$dats
mle.results <- wiki.results$results

errors <- mandelbrot_error(dats, mle.results)

norm_params <- list(mean = mean(errors$Article$log.diff.prob),
                    sd = sqrt(var(errors$Article$log.diff.prob)))


# plot empirical CDF against CDF of normal distribution with
# same mean and std.dev
ggplot(errors$Article) + stat_ecdf(aes(log.diff.prob), pad = T, geom = "step") +
  stat_ecdf(aes(rnorm(283631, mean = norm_params$mean, 
                      sd = norm_params$sd)), 
            pad=T, geom="step") #+  scale_y_log10() + scale_x_log10()

# ks.test against normally distrbuted random samples
# reject hypothesis that distributions are the same if p < \alpha
ks.test(errors$Article$log.diff.prob, 
        rnorm(2836310, mean = norm_params$mean, 
                      sd = norm_params$sd)

# ks.test against theoretical cumulative probability of normal distribution
# reject hypothesis that distributions are the same if p < \alpha
ks.test(errors$Article$log.diff.prob, 
        "pnorm", norm_params$mean, norm_params$sd)

# Q-Q plot with confidence interval
ggplot(errors$Article, aes(sample = log.diff.prob)) + 
  stat_qq(distribution = stats::qnorm, dparams = norm_params) +
  stat_qq_line(distribution = "norm", dparams = norm_params) + 
  stat_qq_band(distribution = "norm", dparams = norm_params)



#scaled.diff <- (errors$Article$log.diff.prob - mean(errors$Article$log.diff.prob))/
#  var(errors$Article$log.diff.prob)


ggplot(data=errors$Article) + 
  geom_hex(aes(log(rank), log.diff.prob), bins=200) + 
  geom_hline(yintercept = 0, color="red") + 
  coord_cartesian(ylim=c(1, -1)) + 
  labs(title=paste("Level: ", "Article"))

last_plot() + geom_hex(data = errors$Paragraph, aes(log(rank), log.diff.prob),
                       bins=200, colour="green")

last_plot() + geom_hex(data = errors$Word, aes(log(rank), log.diff.prob),
                       bins=200, colour="yellow")


glm("count ~ ")


