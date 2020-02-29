export COMMIT_SHA=`git rev-parse HEAD`

# download
#export JOB_NAME=download
#export NUM_JOBS=1
#export PARALLELISM=20
#export SCRIPT=download.py

# transpose
#export JOB_NAME=transpose
#export NUM_JOBS=75
#export PARALLELISM=1
#export SCRIPT=transpose.py

# concat daily chunks
#export JOB_NAME=concat-daily-chunks
#export NUM_JOBS=75
#export PARALLELISM=1
#export SCRIPT=concat-daily-chunks.py

# preprocess
#export JOB_NAME=preprocess
#export NUM_JOBS=1
#export PARALLELISM=20
#export SCRIPT=preprocess.py

# sample stocks
export JOB_NAME=sample-stocks
export NUM_JOBS=27
export PARALLELISM=1
export SCRIPT=sample_stocks.py

mkdir tmp

#for INDEX in {52,60}
for (( INDEX=0; INDEX<NUM_JOBS; INDEX++ ))
do
	sed -e "s|__VERSION__|$COMMIT_SHA|g" -e "s|__INDEX__|$INDEX|g" -e "s|__NUM_JOBS__|$NUM_JOBS|g" -e "s|__JOB_NAME__|$JOB_NAME|g" -e "s|__PARALLELISM__|$PARALLELISM|g" -e "s|__SCRIPT__|$SCRIPT|g" job.yaml | tee tmp/job_$INDEX.yaml
done

#for INDEX in {52,60}
for (( INDEX=0; INDEX<NUM_JOBS; INDEX++ ))
do
	kubectl apply -f tmp/job_$INDEX.yaml
done

#rm -r tmp