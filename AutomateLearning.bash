for run in {1..50}
do
  python RavensProject.py collect && python Answerize.py && rm RawKnownData.csv
done