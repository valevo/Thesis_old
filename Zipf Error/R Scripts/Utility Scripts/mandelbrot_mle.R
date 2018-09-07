# MLE on Mandelbrot
library(stats4)
library(ggplot2)
library(hexbin)
# loads mandel.pdf and mandel.norm
source("probability_definitions.R", chdir = T)
source("util_functions.R", chdir = T)


# function applies MLE for the Mandelbrot model to the three
# levels of splitting to a Wikipedia 
# (see load_wiki_dat for required location and format of data)
# RETURNS: list of 3: MLE object for each splitting level
# NOTE: remove_zero_counts does not make a difference for MLE
#   and does not make a (visible) difference for plots 
#   (log(0) values are removed by dfault)
wiki_mle <- function(language, location="../Estimates", tok="ToktokTokenizer",
                     verbose=TRUE, remove_zero_counts=TRUE, return_data=TRUE){
  
  dats <- load_wiki_dat(folder = location, lang = language, tokenizer = tok, 
                        do_remove = remove_zero_counts)
  
  mle.results <- mandelbrot_mle(dats, verbose = verbose, name = language)
  
  if(return_data){
    return(list(dats = dats, results = mle.results))
  } else return(mle.results)
}

# takes a list of data.frame and performs an MLE for
# the Mandelbrot model; assumes variables rank and count in each
# data.frame
# RETURNS: a list of MLE result objects
mandelbrot_mle <- function(dat_list, verbose=TRUE, name=NULL){
  dat.probs <- function(d, alpha, beta) mandel.pdf(alpha, beta, d$rank)
  get.nLL <- function(dat){
    return(function(alpha, beta) -sum(dat$count*log(dat.probs(dat, alpha, beta))))}
  mle.results <- lapply(dat_list, 
                        function(d){mle(get.nLL(d), 
                                        start = list(alpha = 1, beta = 2))})
  
  if(verbose){
    cat(paste(name, "\n"))
    print(lapply(mle.results, summary))
    plot_mle(dat_list, mle.results, name)
  }
  
  return(mle.results)
}

# takes a list of data.frame (assumes rank and count are present)
# and a list of MLE results (indices in both lists are assumed to correspond)
# and plots rank vs count together with the MLE function
plot_mle <- function(dat_ls, mle_results, name){
  exp.counts <- mapply(get_expected_counts,
                       dat_ls, mle_results, SIMPLIFY = FALSE)
  
  dats.mle <- mapply(function(d, v){data.frame(exp.count = v, rank = d$rank)},
                     dat_ls, exp.counts, SIMPLIFY = FALSE)
  
  if(is.null(names(dat_ls))) { name_ls <- c(1:length(dat_ls))
  } else name_ls <- names(dat_ls)
  for(n in name_ls){
    d <- dat_ls[[n]]
    d.mle <- dats.mle[[n]]
    
    p <- ggplot(d, aes(rank, count)) + geom_hex(bins=75) +
            geom_line(data = d.mle, aes(rank, exp.count), color='red') + 
            scale_y_log10() + scale_x_log10() + 
            labs(title=paste0(name, ": Level: ", n))
    print(p)
  }
}


# take a data.frame dat with columns rank and count
#  and an object of type mle result and returns 
#  a vector with the expected counts (unnormalised by default)
# if max_rank and parameters are given, the expected counts
#  are calculated from the parameters and ranks c(1:max_rank)
get_expected_counts <- function(dat, mle_result, normalised=FALSE, 
                                max_rank=NULL, parameters=NULL){
  if(!is.null(max_rank) && !is.null(parameters)){
    return(mandel.pdf(parameters[["alpha"]], 
                      parameters[["beta"]], c(1:max_rank)))
  }
  alpha <- mle_result@coef["alpha"]
  beta <- mle_result@coef["beta"]
  total_count <- sum(dat$count)
  if(normalised)
    mandel.pdf(alpha, beta, dat$rank)
  else
    mandel.pdf(alpha, beta, dat$rank)*sum(dat$count)
}
