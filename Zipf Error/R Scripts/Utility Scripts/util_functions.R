# file containing unorganised utility functions (declutters other scripts)

# takes a list of data.frames or lists, trims them to equal length,
# and creates a new data.frame with the trimmed frames or lists in it
# RETURNS: data.frame with trimmed combined inputs
unified_df_trim <- function(ls_of_dfs=NULL, ls_of_ls=NULL, given_names=NULL){
  if(!is.null(ls_of_ls)){
    ls_of_dfs <- lapply(ls_of_ls, data.frame)
  }
  smallest <- min(sapply(ls_of_dfs, function(d){dim(d)[1]}))
  unif_dats <- lapply(ls_of_dfs, function(d){d[1:smallest, ]})
  unif_dats <- as.data.frame(do.call(cbind, unif_dats))
  if(!is.null(given_names)){
    names(unif_dats) <- given_names
  }
  names(unif_dats) <- make.unique(names(unif_dats))
  return(unif_dats)
}

# takes a list of data.frames or lists, brings them to equal length,
# based on the mutual intersection of var_to_intersect,
# and creates a new data.frame with the shortened frames or lists in it
# RETURNS: list of data.frame with var_to_intersect equal for all
#   elements
unified_df_intersect <- function(ls_of_dfs, var_to_intersect="word",
                                 given_names=NULL){
  
    var_lists <- lapply(ls_of_dfs, `[[`, var_to_intersect)
    intersection <- Reduce(intersect, var_lists, init = var_lists[[1]])
    print(paste("Size of intersection:", length(intersection)))
    print(paste("Relative sizes: ",
                list((length(intersection)/sapply(ls_of_dfs, dim))[1, ])))
    
    small_dfs <- lapply(ls_of_dfs, 
                        function(d){d[d[[var_to_intersect]] %in% intersection, ]})

    return(small_dfs)
}
  

# calculates the expected value (=mean if probs=NULL)
# RETURNS: double 
expectation <- function(values, probs=NULL){
  if(is.null(probs)){
    probs <- rep(1, length(values))/length(values)
}
  
  return(sum(probs*values))
}

# removes all rows where column var in data.frame df is 0
# if supplied, assigns these rows to zeros_storage so they aren't lost
# RETURNS: the modified data.frame df
remove_zero <- function(df, var="count", how.many=TRUE, keep_zeros=TRUE){
  is_zero <- df[[var]] == 0
  if(how.many){cat("removed: ");cat(length(which(is_zero)))}
  if(keep_zeros){
    cat('\t[Storing zeros in zero_storage]')
    if(exists("zeros_storage")){
      zeros_storage <<- append(zeros_storage, list(df[is_zero, ]))}
    else{zeros_storage <<- list(df[is_zero, ])}} # `<<-` passes changes outside current env
  cat("\n")
  return(df[df[[var]] != 0, ])
}

# IF folder AND lang GIVEN:
#   loads Wiki data files into a named list of data.frame
# IF single_file_name GIVEN:
#   loads the file of that name into a data.frame
# additional parameters for proper loading and preparing
# RETURNS: list of data.frame OR data.frame
load_wiki_dat <- function(folder=NULL, lang=NULL, tokenizer="ToktokTokenizer",
                          header = TRUE, skip = 0, single_file_name=NULL,
                          do_remove=TRUE, store_zeros=TRUE) {
  if(!is.null(folder) && !is.null(lang)){
    split_lvls <- c("Article", "Paragraph", "Word")
    
    file_names <- 
      lapply(split_lvls, function(split_lvl){
        paste(c(folder, "/", lang, "_", tokenizer, "_", split_lvl, "Splitter"), 
        collapse = "")})
  
    dats <- lapply(file_names, 
                 function(name){read.table(name, header = header, skip = skip,
                            comment.char = "", quote = "")})
    
    names(dats) <- split_lvls
    
    if(do_remove){
      dats <- lapply(dats, function(d){remove_zero(d, keep_zeros = store_zeros)})
      names(zeros_storage) <- split_lvls
    }
    return(dats)
  }
  else if(!is.null(single_file_name)){
    dat <- read.table(single_file_name, header = header, skip = skip,
                            comment.char = "", quote = "")
    if(do_remove){dat <- remove_zero(dat, keep_zeros = store_zeros)}
    return(dat)
  }
  else {
    print("The arguments you supplied cannot be used reasonably!")
  }
}

