export COMMIT_SHA=`git rev-parse HEAD`
sed -e "s|__VERSION__|$COMMIT_SHA|g" deployments/job_download_template.yaml | tee deployments/job_download.yaml
kubectl apply -f deployments/job_download.yaml