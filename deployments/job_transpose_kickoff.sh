export COMMIT_SHA=`git rev-parse HEAD`

#for INDEX in {0..74}; do
#  sed -e "s|__VERSION__|$COMMIT_SHA|g" -e "s|__INDEX__|$INDEX|g" deployments/job_transpose_template.yaml | tee deployments/transpose/job_transpose_$INDEX.yaml
#done

for INDEX in {40..74}; do
  kubectl apply -f deployments/transpose/job_transpose_$INDEX.yaml
  rm deployments/transpose/job_transpose_$INDEX.yaml
done

#for INDEX in 3 4 11 17; do
#  kubectl apply -f deployments/transpose/job_transpose_$INDEX.yaml
#  rm deployments/transpose/job_transpose_$INDEX.yaml
#done