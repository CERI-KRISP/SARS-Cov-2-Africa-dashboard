library(ggplot2)
library("readxl")
#library(tidyverse)
library(dplyr)
library(ggpubr)
#library(cowplot)
#library(ggthemes)
#library(viridis)
#library(ggrepel)

args <- commandArgs(trailingOnly = TRUE)
print(args)
data2<-read_excel(args)
data2<-subset(data2,region=='Africa')

# data2<-read_excel('Africa_all_data_15November_gooddates.xlsx')
# data2<-subset(data2,region=='Africa')

df_africa<-data2


df_africa$date<-as.Date(df_africa$date)

df_africa$days<-as.Date(cut(df_africa$date,breaks = "day",start.on.monday = FALSE))
df_africa$date2<-as.Date(cut(df_africa$date,breaks = "2 weeks",start.on.monday = FALSE))
df_africa$date3<-as.Date(cut(df_africa$date,breaks = "1 month",start.on.monday = FALSE))

df_count <- df_africa %>% count(country)
names(df_count)[names(df_count) == "country"] <- "country"
names(df_count)[names(df_count) == "n"] <- "Count"
#df_count

df_africa = df_africa %>% 
  left_join(df_count, by = c("country" = "country"))


df_count[df_count == "Republic of the Congo"] <- "Republic of Congo"
df_count[df_count == "Eswatini"] <- "Swaziland"
#df_count[df_count == "Gambia"] <- "The Gambia"
df_count[df_count == "Guinea-Bissau"] <- "Guinea Bissau"
df_count[df_count == "Cabo Verde"] <- "Cape Verde"
df_count[df_count == "Côte d'Ivoire"] <- "Ivory Coast"
df_count[df_count == "Union of the Comoros"] <- "Comoros"

write.csv(df_africa, "./data/africa.csv", row.names = FALSE)
print("africa.csv updated!")