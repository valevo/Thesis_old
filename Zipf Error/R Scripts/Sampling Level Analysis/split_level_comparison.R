# COMPARE SPLITTING ARTICLES, PARAGRAPHS, AND WORDS
library(ggplot2)

source("util_functions.R")
source("mandelbrot_mle.R")
source("mandelbrot_error.R")

langs <- c("AR", "EO", "EU", "FI","ID","NO","TR", "VI")

for (lang in langs){
wiki.results <- wiki_mle(lang)
dats <- wiki.results$dats
mle.results <- wiki.results$results


# compare empirical CDFs of article, paragraph and word
ecdf_df <- data.frame(frequency = 
                        c(dats$Article$count, dats$Paragraph$count, dats$Word$count),
                      level = factor(c(rep("Article", nrow(dats$Article)), 
                               rep("Paragraph", nrow(dats$Paragraph)),
                               rep("Word", nrow(dats$Word)))))
ggplot(ecdf_df, aes(frequency)) + stat_ecdf(aes(colour=level)) + scale_x_log10() + 
  ylab("probability of frequency") #+ labs(title = paste("Empirical CFDs of", lang))
ggsave0(paste(lang, "_ecdf.pdf"), device = "pdf")

# superimpose estimates from word onto estimates from article
ggplot() + geom_hex(data = dats$Article, aes(rank, count), bins=100, 
                    color="red", show.legend = FALSE) + 
  geom_hex(data = dats$Word, aes(rank, count), bins = 100, 
           color="blue", alpha=I(0.1), show.legend = FALSE) + 
  scale_y_log10() + scale_x_log10() + xlab("frequency")
ggsave(paste0(lang, "_levels_overlay.pdf"), device = "pdf")


# frequency-frequency correlation plot for word and article
unified_dats <- unified_df_intersect(dats)
ggplot() + geom_hex(aes(unified_dats$Article$count, unified_dats$Word$count), 
                    bins=100, show.legend = FALSE) +   scale_x_log10() + scale_y_log10() + 
  ylab("frequency from words") + xlab("frequency from articles") #+ geom_hex(aes(unified_dats$Article$count, unified_dats$Paragraph$count), bins=100, color="red", alpha=I(0.1)) 

ggsave(paste0(lang, "_count_count_corr.pdf"), device = "pdf")
}