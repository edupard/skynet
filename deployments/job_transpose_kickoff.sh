export COMMIT_SHA=`git rev-parse HEAD`
sed -e "s|__VERSION__|$COMMIT_SHA|g" deployments/job_transpose_template.yaml | tee deployments/job_transpose.yaml
kubectl apply -f deployments/job_transpose.yaml
rm deployments/job_transpose.yaml