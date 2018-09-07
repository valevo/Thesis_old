# BAYESIAN MANDELBROT ESTIMATION
require("rjags")
require("ggmcmc")
source("util_functions.R")
source("probability_definitions.R")
source("mandelbrot_mle.R")
library(ggplot2)

model <- "
  model{
    alpha ~ dunif(0, 3)
    beta ~ dunif(0, 5)

    mandel_probs <- pow((ranks + beta), alpha)

    norm <- sum(mandel_probs)

    for(i in 1:n){
      nll[i] <- -counts[i]*log(1/(mandel_probs[i]*norm))
      zeros[i] ~ dpois(nll[i])
    }
  }
"

# zero trick
model2 <- "
  model{
    alpha ~ dunif(0, 3)
    beta ~ dunif(0, 5)

    norm <- sum(pow(ranks + beta, alpha))

    for(i in 1:n){
      prob[i] <- 1/(pow(ranks[i] + beta, alpha)*norm)
      nll[i] <- -counts[i]*log(prob[i])
      zeros[i] ~ dpois(nll[i])
    }
}
"

# ones trick
model3 <- "
  model{
    alpha ~ dunif(0, 3)
    beta ~ dunif(0, 5)

    norm <- sum(pow(ranks + beta, alpha))

    for(i in 1:n){
      word_prob[i] <- 1/(pow(ranks[i] + beta, alpha)*norm)
      count_prob[i] <- pow(word_prob[i], counts[i])
      ones[i] ~ dbern(count_prob[i])
    }
}
"



# ranks <- c(1:10)
# dat <- list(ranks = ranks,
#         counts = c(95356,74479, 71385,56169,55870,55409,41666,38672,34953,31079),
#         n = length(ranks),
#         zeros = rep(0, length(ranks)))

wiki_tab <- load_wiki_dat(
  single_file_name = "../Estimates/AR_ToktokTokenizer_ArticleSplitter")

short_tab <- wiki_tab[1:1000, ]

wiki_mle <- mandelbrot_mle(list(short_tab))

dat <- list(ranks = short_tab$rank,
            counts = short_tab$count,
            n = nrow(short_tab),
            zeros = rep(0, nrow(short_tab)),
            ones = rep(1, nrow(short_tab)))

        
jags_model <- jags.model(textConnection(model3),
                         data =dat, n.adapt = 1000, n.chains = 2)

update(jags_model, 500)

mcmc_samples <- coda.samples(jags_model, c("alpha", "beta", "word_prob"), 500)

ggs_traceplot(ggs(mcmc_samples), family = "nll")

ggs_running(ggs(mcmc_samples), family = "nll")

ggs_density(ggs(mcmc_samples), family = "nll")

ggs_Rhat(ggs(mcmc_samples), family = "alpha")

ggs_autocorrelation(ggs(mcmc_samples), family = "alpha")

ggs_caterpillar(ggs(mcmc_samples), family = "prob", horizontal = F) + 
  scale_x_log10()
