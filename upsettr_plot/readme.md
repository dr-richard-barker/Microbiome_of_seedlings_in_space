## Upsettr plots draft script

**Overview**
data <- read.csv("upset.csv")

expressed = c()
for (colname in colnames(data)){
  if (grepl("GLDS", colname, fixed = TRUE) && !grepl("Expression", colname, fixed = TRUE)){
    expressed <- c(expressed, colname)
  }
}

upset(data, sets=expressed)

**Breakdown**
ggplot(data=expressions, aes(x=Total, y=n, fill=GLDS218Expression)) + 
     geom_bar(stat="identity") +
         theme_minimal()


kable(expressions) %>%  kable_styling("striped", full_width = F)

table_df %>%
kable(format = "html", escape = F) %>%
  kable_styling("striped", full_width = F) %>%
   row_spec(0, bold = T, color = "black", background = "#FFFFF") %>%
    scroll_box(width = "100%", height = "1000px")


![Upsettr_plot_OSDR_5_studies](https://github.com/dr-richard-barker/MATRIX5_pseudo_time-series/assets/8679982/6190e7b7-80db-4142-992f-41b6e32828a6)
