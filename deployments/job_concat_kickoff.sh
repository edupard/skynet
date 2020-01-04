export COMMIT_SHA=`git rev-parse HEAD`
sed -e "s|__VERSION__|$COMMIT_SHA|g" deployments/job_concat_template.yaml | tee deployments/job_concat.yaml
kubectl apply -f deployments/job_concat.yaml
rm deployments/job_concat.yaml