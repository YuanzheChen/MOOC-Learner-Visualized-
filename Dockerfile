FROM visualized:base
RUN mkdir app
ADD . /app/MOOC-Learner-Visualized
WORKDIR /app/MOOC-Learner-Visualized
RUN ["chmod", "+x", "wait_for_it.sh"]
CMD ["./wait_for_it.sh", "quantified", "python", "-u", "autorun.py", "-c", "../config/config.yml"]
