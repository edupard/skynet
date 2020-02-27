export COMMIT_SHA=`git rev-parse HEAD`

export NUM_WORKERS=75

for INDEX in {0..$[NUM_WORKERS - 1]}; do
  sed -e "s|__VERSION__|$COMMIT_SHA|g" -e "s|__INDEX__|$INDEX|g" -e "s|__NUM_WORKERS__|$NUM_WORKERS|g" deployments/transpose.yaml | tee deployments/tmp/job_$INDEX.yaml
done

for INDEX in {0..$[NUM_WORKERS - 1]}; do
  kubectl apply -f deployments/tmp/job_$INDEX.yaml
  rm deployments/tmp/job_$INDEX.yaml
done