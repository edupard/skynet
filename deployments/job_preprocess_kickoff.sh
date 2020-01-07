export COMMIT_SHA=`git rev-parse HEAD`
sed -e "s|__VERSION__|$COMMIT_SHA|g" deployments/job_preprocess_template.yaml | tee deployments/job_preprocess.yaml
kubectl apply -f deployments/job_preprocess.yaml
rm deployments/job_preprocess.yaml