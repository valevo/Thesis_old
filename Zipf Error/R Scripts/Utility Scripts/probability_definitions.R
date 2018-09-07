mandel.norm <- function(alpha, beta, ranks) sum(1/(ranks + beta)^alpha)

mandel.pdf <- function(alpha, beta, ranks){
  1/((ranks + beta)^alpha)/mandel.norm(alpha, beta, ranks)
}


# (N,alpha)-harmonic number
zipf.norm <- function(alpha, N) sum(1/(c(1:N)^alpha))

# P(W = w_r| alpha)
zipf.pdf <- function(alpha, ranks){(1/(ranks^alpha)/zipf.norm(alpha, max(ranks)))}

