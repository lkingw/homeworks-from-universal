library(mice) #deal with missing data
library(corrplot) #plot for correlation matrix
library(ggplot2) #visualization and plots
library(scales) #graphical scales map data to aesthetics
library(dplyr) #data manipulation: filter and arrange
library(tidyverse) #data manipulation
library(VIM) #tools for the visualization of missing or imputed values

df <- read.csv("wine.csv")
df <- df[,-7]
dim(df)

str(df)
summary(df)

#Checking missing values
aggr_plot <- aggr(df, col=c('navyblue','red'), numbers=TRUE, sortVars=TRUE, labels=names(df), cex.axis=.7, gap=3, ylab=c("Histogram of missing data","Pattern"))

#Build correlation and order by decreasing
set.seed(123)
library(dplyr)
library(tidyr)
cor(df) %>%
  as.data.frame() %>%
  mutate(var1 = rownames(.)) %>%
  gather(var2, value, -var1) %>%
  arrange(desc(value)) %>%
  group_by(value) %>%
  filter(row_number()==1)

#draw correlation matrix
dfcor <- cor(df)
corrplot(dfcor, method = "color", addCoef.col = "black",number.cex = .6,
         tl.col = "black", tl.srt = 90, diag = FALSE)

#overall quality
q1 <- ggplot(df, aes(price))+ 
  geom_histogram() + 
  labs(title = "Histogram of price") + 
  theme(plot.title=element_text(hjust=0.5)) +
  geom_vline(aes(xintercept=mean(price)), color="blue", linetype="dashed", size=1) +
  geom_text(aes(x=22, label="Mean Value", y=6), colour="red", angle=90, vjust = 1.2, text=element_text(size=11))
q1
q2 <- ggplot(df, aes(sample=price)) +
  stat_qq(color="dodgerblue4") + 
  stat_qq_line(color="red") +
  scale_y_continuous(labels=function(y){y/10^6}) +
  labs(title="QQ Plot for quality", y="Ordered Values") +
  theme(plot.title=element_text(hjust=0.5))
q2

#univariate analysis
p1 <- ggplot(df, aes(x=h.rain)) + 
  geom_density()
p1 + geom_vline(aes(xintercept=mean(h.rain)),
                color="blue", linetype="dashed", size=1)
p2 <- ggplot(df, aes(x=s.temp)) + 
  geom_density()
p2 + geom_vline(aes(xintercept=mean(s.temp)),
                color="blue", linetype="dashed", size=1)
p3 <- ggplot(df, aes(x=w.rain)) + 
  geom_density()
p3 + geom_vline(aes(xintercept=mean(w.rain)),
                color="blue", linetype="dashed", size=1)
p4 <- ggplot(df, aes(x=h.temp)) + 
  geom_density()
p4 + geom_vline(aes(xintercept=mean(h.temp)),
                color="blue", linetype="dashed", size=1)
p5 <- ggplot(df, aes(x=year)) + 
  geom_density()
p5 + geom_vline(aes(xintercept=mean(year)),
                color="blue", linetype="dashed", size=1)
ggarrange(p1, p2, p3, p4, p5, nrow = 2, ncol =3)

#bivariate analysis
g1 <- ggplot(data = df, mapping = aes(x = h.rain, y = price)) + geom_point() + stat_smooth()
g2 <- ggplot(data = df, mapping = aes(x = s.temp, y = price)) + geom_point() + stat_smooth()
g3 <- ggplot(data = df, mapping = aes(x = w.rain, y = price)) + geom_point() + stat_smooth()
g4 <- ggplot(data = df, mapping = aes(x = h.temp, y = price)) + geom_point() + stat_smooth()
g5 <- ggplot(data = df, mapping = aes(x = year, y = price)) + geom_point() + stat_smooth()
ggarrange(g1, g2, g3, g4, g5, nrow = 2, ncol =3)

#build liner gression model
lm1 <- lm(price ~ h.rain + s.temp + w.rain + h.temp + year, data = df)
anova(lm1)
summary(lm1)

#residual analysis
par(mfrow=c(2,2))
plot(lm1)