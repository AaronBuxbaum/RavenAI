for run in {1..1}
do
  python RavensProject.py collect && python Answerize.py && rm RawKnownData.csv
done