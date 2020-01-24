export COMMIT_SHA=`git rev-parse HEAD`

for INDEX in {0..0}; do
  sed -e "s|__VERSION__|$COMMIT_SHA|g" -e "s|__INDEX__|$INDEX|g" deployments/job_samples_data_template.yaml | tee deployments/tmp/job_$INDEX.yaml
done

for INDEX in {0..0}; do
  kubectl apply -f deployments/tmp/job_$INDEX.yaml
  rm deployments/tmp/job_$INDEX.yaml
done