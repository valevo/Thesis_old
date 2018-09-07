# BAYESIAN CORRELATION
library(ggplot2)
require("rjags")
require("ggmcmc")

bayes.correlation <- function(v1, v2, vars_to_get){
  model <- "
    model {
      # priors
      # CHANGE
      mu[1] ~ dnorm(0, 0.001)
      mu[2] ~ dnorm(0, 0.001)
      sigma[1] ~ dunif(0, 1000) 
      sigma[2] ~ dunif(0, 1000)
      rho ~ dunif(-1, 1)
    
      # Constructing the covariance matrix and the corresponding precision matrix.
      cov[1,1] <- sigma[1] * sigma[1]
      cov[1,2] <- sigma[1] * sigma[2] * rho
      cov[2,1] <- sigma[1] * sigma[2] * rho
      cov[2,2] <- sigma[2] * sigma[2]
      prec[1:2,1:2] <- inverse(cov[,])
    
      for(i in 1:n) {
        x[i,1:2] ~ dmnorm(mu[], prec[ , ])
      }
  
      # Generate random draws from the estimated bivariate normal distribution
      # x_rand ~ dmnorm(mu[], prec[ , ])
  }
  "
  dat <- cbind(v1, v2)  
  data_list = list(x = dat, n = nrow(dat))
  # Use classical estimates of the parameters as initial values
  inits_list = list(mu = c(mean(v1), mean(v2)),
                    rho = cor(v1, v2),
                    sigma = c(sd(v1), sd(v2)))
  jags_model <- jags.model(textConnection(model), 
                           data = data_list, inits = inits_list,
                           n.adapt = 500, n.chains = 2, quiet = F)
  update(jags_model, 500)
  return(coda.samples(jags_model, vars_to_get,
                               n.iter = 100))
}

x <- rnorm(1000)
y <- rnorm(1000)

jags_samples <- bayes.correlation(x, y, c("rho", "mu"))

ggs_traceplot(ggs(jags_samples))

ggs_density(ggs(jags_samples), family = "rho")
ggs_density(ggs(jags_samples), family = "mu")
