export COMMIT_SHA=`git rev-parse HEAD`
sed -e "s|__VERSION__|$COMMIT_SHA|g" deployments/job_samples_data_concat_template.yaml | tee deployments/tmp/job.yaml
kubectl apply -f deployments/tmp/job.yaml
rm deployments/tmp/job.yaml