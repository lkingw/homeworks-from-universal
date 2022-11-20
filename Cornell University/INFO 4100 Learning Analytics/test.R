library(tidyverse)
library(dplyr)
library(ggplot2)

load("info4100.proj.dashboard.rda")

combined_allyears = full_join(x = quiz, y = select(experience, !"YEAR"), by = "STUDENT_KEY", copy = F, keep = F)
nice_data =  combined_allyears %>% filter(!is.na(combined_allyears$QUIZ_SCORE))

avg_quiz_data = nice_data %>% select(PROG, YEAR, QUIZ_SCORE) %>%
  group_by(YEAR, PROG) %>%
  summarise(
    avg_quiz_score = mean(QUIZ_SCORE)
)

attendance_rate = nice_data %>% select(SESSION_NUMBER, ATTENDED, STUDENT_KEY, YEAR) %>%
  group_by(SESSION_NUMBER, YEAR) %>%
  summarise(
    attendance_per_session = sum(ATTENDED) / n()
)

nice_data$YEAR = paste0('_', nice_data$YEAR)

ggplot(attendance_rate, aes(x=SESSION_NUMBER, y=attendance_per_session, group=YEAR, color=YEAR)) +
  labs(y = "Attendance Rate", x = "Session Number") +
  geom_line()

ggplot(avg_quiz_data, aes(fill=PROG, y=avg_quiz_score, x=YEAR)) +
  labs(y = "Quiz Score (AVG)", x = "Year") +
  geom_bar(position="dodge", stat="identity")
#avg iclick grade per lecture2
