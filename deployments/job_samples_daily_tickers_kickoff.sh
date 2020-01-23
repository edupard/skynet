export COMMIT_SHA=`git rev-parse HEAD`
sed -e "s|__VERSION__|$COMMIT_SHA|g" deployments/job_samples_daily_tickers_template.yaml | tee deployments/job_samples_daily_tickers.yaml
kubectl apply -f deployments/job_samples_daily_tickers.yaml
rm deployments/job_samples_daily_tickers.yaml