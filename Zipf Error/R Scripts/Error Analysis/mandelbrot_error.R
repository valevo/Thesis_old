# obtaining and plotting error of MLE on Mandelbrot
library(stats4)
library(ggplot2)
library(hexbin)
# loads mandel.pdf and mandel.norm
source("../Utility Scripts/probability_definitions.R")
source("../Utility Scripts/util_functions.R")
source("../Utility Scripts/mandelbrot_mle.R")


probs_from_mle <- function(results, dats, coef_ls = list("alpha", "beta"), 
                           use_ranks=TRUE){
  coefs <- lapply(list("alpha", "beta"), 
                  function(c){lapply(results, 
                                     function(res){res@coef[c]})})
  if(use_ranks){ ranks <- lapply(dats, `[[`, "rank")
    }else ranks <- lapply(dats, function(d){c(1:max(d$rank))})
    
  probs <- mapply(function(a, b, r){mandel.pdf(a, b, r)}, 
                  coefs[[1]], coefs[[2]], ranks, SIMPLIFY = FALSE)
  return(probs)
}

mandelbrot_error <- function(dat_ls, mle_result_ls, verbose=TRUE){
  theoretical_probs <- probs_from_mle(mle_result_ls, dat_ls)
  err.dats <- mapply(function(d, p){
    data.frame(rank = d$rank, emp.prob = d$count/sum(d$count), theo.prob = p, 
               exp.count = sum(d$count)*p,
               log.diff.prob = log(p/(d$count/sum(d$count)))#,log.diff.prob = log(d$count/sum(d$count)) - log(p)
    )},
    dat_ls, theoretical_probs, SIMPLIFY = FALSE)
  
  if(verbose){
    if(is.null(names(dat_ls))) { name_ls <- c(1:length(dat_ls))
    } else name_ls <- names(dat_ls)
    
    for(n in name_ls){
      plot_mandelbrot_error(err.dats[[n]], n)
    }
  }
  
  return(err.dats)
}

plot_mandelbrot_error <- function(error_frame, name, do_plot=TRUE,
                                  plot_line = TRUE){
  p <- ggplot(data=error_frame) + 
          geom_hex(aes(log(rank), log.diff.prob), bins=200) + 
          coord_cartesian(ylim=c(1, -1)) + 
          labs(title=paste("Level: ", name))
  
  if (plot_line){p <- p  + geom_hline(yintercept = 0, color="red")}
  if (do_plot) { print(p)}
  return(p)
}

count_err_dist <- function(error_frame, do_plot=TRUE) {
  distr <- lapply(sort(unique(error_frame$count)), 
                  function(f){error_frame[error_frame$count == f, 5]})
  
  names(distr) <- sort(unique(error_frame$count))
  c_errs <- data.frame(count=sort(unique(error_frame$count)), 
                       mins=sapply(distr, min),
                       means=sapply(distr, median),
                       maxs=sapply(distr, max))
  
  if (do_plot){
    p <- ggplot(c_errs, aes(x=log(count), y=means)) + 
          geom_point(size=0.2)+
          geom_errorbar(aes(ymin=mins, ymax=maxs), size=0.2) + 
          geom_smooth(method = "loess", span=0.1)+
          scale_x_reverse() + coord_cartesian(ylim = c(-1, 1))
    print(p)}
  
  return(distr)
}


KL_div <- function(emp_probs, theo_probs){
  -expectation(log(theo_probs/emp_probs), probs = emp_probs)
}



# WITHOUT THE ZEROS (i.e. removing all r s.t. c_r = 0)
# all r s.t. c_r = 0  will lead to theo.prob/emp.prob undefined
# language <- "ID"
# mle <- wiki_mle(language)
# dats <- mle$dats
# mle.results <- mle$results
# 
# err.dats <- mandelbrot_error(dats, mle.results)
# last_plot() + geom_smooth(aes(log(rank), log.diff.prob))

# ggplot(err.dats$Word) + stat_ecdf(aes(emp.prob), geom="step") + 
#   scale_y_log10() + scale_x_log10()
# 
# ggplot(err.dats$Word) + geom_point(aes(seq_along(emp.prob), emp.prob))
