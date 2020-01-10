export COMMIT_SHA=`git rev-parse HEAD`
sed -e "s|__VERSION__|$COMMIT_SHA|g" deployments/job_samples_template.yaml | tee deployments/job_samples.yaml
kubectl apply -f deployments/job_samples.yaml
rm deployments/job_samples.yaml