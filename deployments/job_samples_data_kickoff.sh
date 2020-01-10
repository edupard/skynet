export COMMIT_SHA=`git rev-parse HEAD`
sed -e "s|__VERSION__|$COMMIT_SHA|g" deployments/job_samples_data_template.yaml | tee deployments/job_samples_data.yaml
kubectl apply -f deployments/job_samples_data.yaml
rm deployments/job_samples_data.yaml