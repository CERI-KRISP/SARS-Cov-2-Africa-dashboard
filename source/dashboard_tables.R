#!/bin/sh
pkgLoad <- function( packages = "favorites" ) {

    if( length( packages ) == 1L && packages == "favorites" ) {
        packages <- c( "readr", "dplyr", "tidyr", "lubridate")
    }

    packagecheck <- match( packages, utils::installed.packages()[,1] )

    packagestoinstall <- packages[ is.na( packagecheck ) ]

    if( length( packagestoinstall ) > 0L ) {
        utils::install.packages( packagestoinstall,
                             repos = "http://cran.r-project.org"
        )
    } else {
        print( "All requested packages already installed" )
    }

    for( package in packages ) {
        suppressPackageStartupMessages(
            library( package, character.only = TRUE, quietly = TRUE )
        )
    }

}
#Load libraries
# library(readr)
# library(dplyr)
# library(tidyr)
# library(lubridate)

#read data file
Africa_df <- read.csv("data/all_data_processed.csv")

#sorting by date to simplify extraction for first and most recent sample collection
#ymd function requires date formatted with any separator but as YYYY-MM-DD, previously date had been in dmy format as DD-MM-YYYY
Africa_df$collection_date<-lubridate::ymd(Africa_df$collection_date)
Africa_df$subm_date<-ymd(Africa_df$subm_date)
Africa_df <- Africa_df[order(Africa_df$collection_date),]
#remove missing/incorrectly formatted dates
cutoff=lubridate::ymd("2018-01-01")
Africa_df <- filter(Africa_df, collection_date>cutoff)

#sorting data into variant specific frames, removed preprocessing step as it isn't necessary anymore. 
#note non-voc/voi data is no longer stored
alpha_data <- Africa_df[Africa_df$variant=="Alpha",]
beta_data <- Africa_df[Africa_df$variant=="Beta",]
delta_data <- Africa_df[Africa_df$variant=="Delta",]
omicron_data <- Africa_df[Africa_df$variant=="Omicron",]
a231_data <- Africa_df[Africa_df$variant_GISAID_name=="A.23.1",]
b11318_data <- Africa_df[Africa_df$variant_GISAID_name=="B.1.1.318",]
c1_data <- Africa_df[Africa_df$variant_GISAID_name=="C.1",]
c12_data <- Africa_df[Africa_df$variant_GISAID_name=="C.1.2",]
c363_data <- Africa_df[Africa_df$variant_GISAID_name=="C.36.3",]
eta_data <- Africa_df[Africa_df$variant_GISAID_name=="VOI Eta G/484K.V3 (B.1.525) first detected in UK/Nigeria",]

#earliest sample collection
FirstSequence <-c(alpha_data[1,2],beta_data[1,2],delta_data[1,2],omicron_data[1,2],a231_data[1,2],b11318_data[1,2],c1_data[1,2],c12_data[1,2],c363_data[1,2],eta_data[1,2])
#most recent sample collection
LastSequence <-c(alpha_data[nrow(alpha_data),2],beta_data[nrow(beta_data),2],delta_data[nrow(delta_data),2],omicron_data[nrow(omicron_data),2],a231_data[nrow(a231_data),2],b11318_data[nrow(b11318_data),2],c1_data[nrow(c1_data),2],c12_data[nrow(c12_data),2],c363_data[nrow(c363_data),2],eta_data[nrow(eta_data),2])

#new submissions in past 30 days
curr_date=Sys.Date()-30
alphap30 <- filter(alpha_data, subm_date>=curr_date)
betap30 <-filter(beta_data, subm_date>=curr_date)
deltap30 <-filter(delta_data, subm_date>=curr_date)
omicronp30 <-filter(omicron_data, subm_date>=curr_date)
a231p30 <-filter(a231_data, subm_date>=curr_date)
b11318p30 <-filter(b11318_data, subm_date>=curr_date)
c1p30 <-filter(c1_data, subm_date>=curr_date)
c12p30 <-filter(c12_data, subm_date>=curr_date)
c363p30 <-filter(c363_data, subm_date>=curr_date)
etap30 <-filter(eta_data, subm_date>=curr_date)

#new samples in past 30 days
alphacp30 <- filter(alpha_data, collection_date>=curr_date)
betacp30 <-filter(beta_data, collection_date>=curr_date)
deltacp30 <-filter(delta_data, collection_date>=curr_date)
omicroncp30 <-filter(omicron_data, collection_date>=curr_date)
a231cp30 <-filter(a231_data, collection_date>=curr_date)
b11318cp30 <-filter(b11318_data, collection_date>=curr_date)
c1cp30 <-filter(c1_data, collection_date>=curr_date)
c12cp30 <-filter(c12_data, collection_date>=curr_date)
c363cp30 <-filter(c363_data, collection_date>=curr_date)
etacp30 <-filter(eta_data, collection_date>=curr_date)

#find lineage names, combine into single string for ease of tabulation
alpha_lineage <- paste(unlist(as.character(unique(alpha_data$lineage))),collapse=", ")
beta_lineage <- paste(unlist(as.character(unique(beta_data$lineage))),collapse=", ")
delta_lineage <- paste(unlist(as.character(unique(delta_data$lineage))),collapse=", ")
omicron_lineage <- paste(unlist(as.character(unique(omicron_data$lineage))),collapse=", ")
a231_lineage <- paste(unlist(as.character(unique(a231_data$lineage))),collapse=", ")
b11318_lineage <- paste(unlist(as.character(unique(b11318_data$lineage))),collapse=", ")
c1_lineage <- paste(unlist(as.character(unique(c1_data$lineage))),collapse=", ")
c12_lineage <- paste(unlist(as.character(unique(c12_data$lineage))),collapse=", ")
c363_lineage <- paste(unlist(as.character(unique(c363_data$lineage))),collapse=", ")
eta_lineage <- paste(unlist(as.character(unique(eta_data$lineage))),collapse=", ")


#create column vectors for tibble (retains date format the best)
cd=lubridate::ymd(Sys.Date())
Variants<-c('Alpha', 'Beta','Delta','Omicron','A.23.1','B.1.1.318','C.1','C.1.2','C.36.3','Eta')
#alternative name column no longer needed
#Alternative_names<-c("VOC-2020-12-01","VOC-2020-12-02", "VOC-2021-03-02", "VOC-2021-11-26", "NA", "VUM-2021-06-04", "NA", "VUM-2021-09-01", "VUM-2021-06-16", "VUM-2021-02-03")
Lineage_sublineage<-c(alpha_lineage,beta_lineage,delta_lineage,omicron_lineage, a231_lineage,b11318_lineage,c1_lineage,c12_lineage,c363_lineage,eta_lineage)
Total_Confirmed<-c(nrow(alpha_data), nrow(beta_data), nrow(delta_data), nrow(omicron_data), nrow(a231_data), nrow(b11318_data), nrow(c1_data), nrow(c12_data), nrow(c363_data), nrow(eta_data))
SeqsPast30<-c(nrow(alphap30), nrow(betap30), nrow(deltap30), nrow(omicronp30), nrow(a231p30), nrow(b11318p30), nrow(c1p30), nrow(c12p30), nrow(c363p30), nrow(etap30))
SamplesPast30<-c(nrow(alphacp30), nrow(betacp30), nrow(deltacp30), nrow(omicroncp30), nrow(a231cp30), nrow(b11318cp30), nrow(c1cp30), nrow(c12cp30), nrow(c363cp30), nrow(etacp30))
#Dayssince refers to days since last sample collection, this was previously in the third column but is now in the second.
DaysSince<-c(cd-alpha_data[nrow(alpha_data),2], cd-beta_data[nrow(beta_data),2], cd-delta_data[nrow(delta_data),2], cd-omicron_data[nrow(omicron_data),2], cd-a231_data[nrow(a231_data),2], cd-b11318_data[nrow(b11318_data),2], cd-c1_data[nrow(c1_data),2], cd-c12_data[nrow(c12_data),2], cd-c363_data[nrow(c363_data),2], cd-eta_data[nrow(eta_data),2])

alldata<- tibble(Variants,Lineage_sublineage,Total_Confirmed,SeqsPast30,SamplesPast30,FirstSequence,LastSequence,DaysSince)

write.csv(alldata, file = "data/variants_summary_table.csv")

