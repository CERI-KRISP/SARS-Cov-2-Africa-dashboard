#Load libraries
library(readr)
library(dplyr)
library(tidyr)
library(lubridate)
#read data file
Africa_df <- read.csv("df_africa.csv")

#create buckets for and clade assignment
alpha <- c("VOC Alpha GRY (B.1.1.7+Q.*) first detected in the UK")
beta <- c("VOC Beta GH/501Y.V2 (B.1.351+B.1.351.2+B.1.351.3) first detected in South Africa")
delta <- c("VOC Delta GK (B.1.617.2+AY.*) first detected in India")
omicron <- c("VOC Omicron GRA (B.1.1.529+BA.*) first detected in Botswana/Hong Kong/South Africa")
a.23.1 <- c("A.23.1")
b.1.1.318 <- c("B.1.1.318")
c.1 <- c("C.1")
c.1.2 <- c("C.1.2")
c.36.3 <- c("C.36.3")
eta <- c("VOI Eta G/484K.V3 (B.1.525) first detected in UK/Nigeria")

#bin data into buckets
Africa_df <- Africa_df %>% mutate(variant_clade = ifelse(Africa_df$covv_variant %in% alpha, "Alpha", ifelse(
                                    Africa_df$covv_variant %in% beta, "Beta", ifelse(
                                      Africa_df$covv_variant %in% delta, "Delta", ifelse(
                                        Africa_df$covv_variant %in% omicron, "Omicron", ifelse(
                                          Africa_df$covv_variant %in% a.23.1, "A.23.1", ifelse(
                                            Africa_df$covv_variant %in% b.1.1.318, "B.1.1.318", ifelse(
                                              Africa_df$covv_variant %in% c.1, "C.1", ifelse(
                                                Africa_df$covv_variant %in% c.1.2, "C.1.2", ifelse(
                                                  Africa_df$covv_variant %in% c.36.3, "C.36.3", ifelse(
                                                    Africa_df$covv_variant %in% eta, "Eta", "Other Lineages"
                                  )))))))))))
                                  
#sorting by date to simplify extraction for first and most recent sample collection

Africa_df$covv_collection_date<-dmy(Africa_df$covv_collection_date)
Africa_df$covv_subm_date<-dmy(Africa_df$covv_subm_date)
Africa_df <- Africa_df[order(Africa_df$covv_collection_date),]
#remove missing/incorrectly formatted dates
cutoff=dmy("01-01-2018")
Africa_df <- filter(Africa_df, covv_collection_date>cutoff)

#sorting data into variant specific frames (potential space to parallelise task)
alpha_data <- Africa_df[Africa_df$variant_clade=="Alpha",]
beta_data <- Africa_df[Africa_df$variant_clade=="Beta",]
delta_data <- Africa_df[Africa_df$variant_clade=="Delta",]
omicron_data <- Africa_df[Africa_df$variant_clade=="Omicron",]
a231_data <- Africa_df[Africa_df$variant_clade=="A.23.1",]
b11318_data <- Africa_df[Africa_df$variant_clade=="B.1.1.318",]
c1_data <- Africa_df[Africa_df$variant_clade=="C.1",]
c12_data <- Africa_df[Africa_df$variant_clade=="C.1.2",]
c363_data <- Africa_df[Africa_df$variant_clade=="C.36.3",]
eta_data <- Africa_df[Africa_df$variant_clade=="Eta",]
other_data <- Africa_df[Africa_df$variant_clade=="Other Lineages",]

#earliest sample collection
firstSequence <-c(alpha_data[1,3],beta_data[1,3],delta_data[1,3],omicron_data[1,3],a231_data[1,3],b11318_data[1,3],c1_data[1,3],c12_data[1,3],c363_data[1,3],eta_data[1,3])
#most recent sample collection
lastSequence <-c(alpha_data[nrow(alpha_data),3],beta_data[nrow(beta_data),3],delta_data[nrow(delta_data),3],omicron_data[nrow(omicron_data),3],a231_data[nrow(a231_data),3],b11318_data[nrow(b11318_data),3],c1_data[nrow(c1_data),3],c12_data[nrow(c12_data),3],c363_data[nrow(c363_data),3],eta_data[nrow(eta_data),3])

#new submissions in past 30 days
curr_date=Sys.Date()-30
alphap30 <- filter(alpha_data, covv_subm_date>=curr_date)
betap30 <-filter(beta_data, covv_subm_date>=curr_date)
deltap30 <-filter(delta_data, covv_subm_date>=curr_date)
omicronp30 <-filter(omicron_data, covv_subm_date>=curr_date)
a231p30 <-filter(a231_data, covv_subm_date>=curr_date)
b11318p30 <-filter(b11318_data, covv_subm_date>=curr_date)
c1p30 <-filter(c1_data, covv_subm_date>=curr_date)
c12p30 <-filter(c12_data, covv_subm_date>=curr_date)
c363p30 <-filter(c363_data, covv_subm_date>=curr_date)
etap30 <-filter(eta_data, covv_subm_date>=curr_date)

#new samples in past 30 days
alphacp30 <- filter(alpha_data, covv_collection_date>=curr_date)
betacp30 <-filter(beta_data, covv_collection_date>=curr_date)
deltacp30 <-filter(delta_data, covv_collection_date>=curr_date)
omicroncp30 <-filter(omicron_data, covv_collection_date>=curr_date)
a231cp30 <-filter(a231_data, covv_collection_date>=curr_date)
b11318cp30 <-filter(b11318_data, covv_collection_date>=curr_date)
c1cp30 <-filter(c1_data, covv_collection_date>=curr_date)
c12cp30 <-filter(c12_data, covv_collection_date>=curr_date)
c363cp30 <-filter(c363_data, covv_collection_date>=curr_date)
etacp30 <-filter(eta_data, covv_collection_date>=curr_date)

#create column vectors for tibble (retains date format the best)
cd=Sys.Date()
Variants<-c('Alpha', 'Beta','Delta','Omicron','A.23.1','B.1.1.318','C.1','C.1.2','C.36.3','Eta')
Alternative_names<-c("VOC-2020-12-01","VOC-2020-12-02", "VOC-2021-03-02", "VOC-2021-11-26", "NA", "VUM-2021-06-04", "NA", "VUM-2021-09-01", "VUM-2021-06-16", "VUM-2021-02-03")
Lineage_sublineage<-c('B.1.1.7, AZ.X','B.1.351, B1.351.X','B.1.617.2, AY.X','B.1.1.529, BA.X', 'A.23.1','B.1.1.318','C.1','C.1.2','C.36.3','B.1.525')
Total_Confirmed<-c(nrow(alpha_data), nrow(beta_data), nrow(delta_data), nrow(omicron_data), nrow(a231_data), nrow(b11318_data), nrow(c1_data), nrow(c12_data), nrow(c363_data), nrow(eta_data))
SeqsPast30<-c(nrow(alphap30), nrow(betap30), nrow(deltap30), nrow(omicronp30), nrow(a231p30), nrow(b11318p30), nrow(c1p30), nrow(c12p30), nrow(c363p30), nrow(etap30))
SamplesPast30<-c(nrow(alphacp30), nrow(betacp30), nrow(deltacp30), nrow(omicroncp30), nrow(a231cp30), nrow(b11318cp30), nrow(c1cp30), nrow(c12cp30), nrow(c363cp30), nrow(etacp30))
DaysSince<-c(cd-alpha_data[nrow(alpha_data),3], cd-beta_data[nrow(beta_data),3], cd-delta_data[nrow(delta_data),3], cd-omicron_data[nrow(omicron_data),3], cd-a231_data[nrow(a231_data),3], cd-b11318_data[nrow(b11318_data),3], cd-c1_data[nrow(c1_data),3], cd-c12_data[nrow(c12_data),3], cd-c363_data[nrow(c363_data),3], cd-eta_data[nrow(eta_data),3])

alldata<- tibble(Variants,Alternative_names,Lineage_sublineage,Total_Confirmed,SeqsPast30,SamplesPast30,firstSequence,lastSequence,DaysSince)
write.csv(alldata, file = "AllVariantsTable.csv")

