########## Code for extracting the XML data and organizing the initial dataframe ##########
# Note: some minor edits were made to the original XML file before the importation process.

### IMPORT XML DATA
library(XML)
doc = xmlParse("resources/EFCAMDAT_Shatz-2020_distro/Main\ data\ at\ different\ stages/EFCAMDAT_full_data_file.xml")

### BIND ATTRIBUTES AND ELEMENTS
xml_df <- cbind(XML:::xmlAttrsToDataFrame(getNodeSet(doc, path='//writing')),
                XML:::xmlAttrsToDataFrame(getNodeSet(doc, path='//learner')),
                XML:::xmlAttrsToDataFrame(getNodeSet(doc, path='//topic')),
                xmlToDataFrame(doc, nodes = getNodeSet(doc, "//writing"))
)    


### RENAME COLUMNS
xml_df <- setNames(xml_df, c("writing_id", "level", "unit", "learner_id", "nationality",
                             "topic_id", "EMPTY", "topic", "date", "grade", "text"))


###  REMOVE REDUNDANT COLUMN
xml_df$EMPTY <- NULL

write.csv(xml_df, 'resources/EFCAMDAT_data.csv', row.names = FALSE)

