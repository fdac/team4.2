require(ggplot2)

setwd('~/Google Drive/UTK/Fall 2014/COSC 594/Project 2/')
data <- read.csv('usermetrics.csv', head=T, sep=';')
data$logContrib <- ifelse(data$numContrib==0, 0, log(data$numContrib))
data$logQuality <- ifelse(data$numQuality==0, 0, log(data$numQuality))

### this is the plot of the data
p <- ggplot(data, aes(logContrib, logQuality))
p <- p + geom_point(size=3, alpha=.2) ## alpha controls the opacity of each point. it takes values from 0 (transparent) to 1 (opaque).
p

### this section displays the names of users for different areas of the plot above
data2 <- data[data$logQuality>=4.1 & data$logContrib>=8,]
data3 <- data[data$logQuality>=1 & data$logContrib>=7.5,]
data4 <- data[data$logQuality>=1 & data$logContrib<=7.5 & data$logContrib>=2.5,]
