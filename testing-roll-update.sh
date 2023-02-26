#!/usr/local/bin/bash

#export HTTPS_PROXY=http://LPGPZENPROXY.EMEA.LEASEPLANCORP.NET:80
#export https_proxy=http://LPGPZENPROXY.EMEA.LEASEPLANCORP.NET:80
#export HTTP_PROXY=http://LPGPZENPROXY.EMEA.LEASEPLANCORP.NET:80
#export http_proxy=http://LPGPZENPROXY.EMEA.LEASEPLANCORP.NET:80
#export no_proxy=localhost,127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,core-services.leaseplan.systems

export K8S_PROXY_BYPASS=true

export AWS_REGION="${AWS_REGION:-eu-west-1}"
export AWS_DEFAULT_REGION=$AWS_REGION
export AWS_PROFILE="devops@sandbox.digital"

export ENV_PREFIX="${ENV_PREFIX:-lpd}"
export ENVIRONMENT="${ENVIRONMENT:-sandbox}"

export PYTHONPATH=${PYTHONPATH}:../eks-rolling-update

export RUN_MODE="${RUN_MODE:-4}"
#export DRY_RUN="${DRY_RUN:-true}"
export DRY_RUN="${DRY_RUN:-false}"
export GLOBAL_MAX_RETRY="${GLOBAL_MAX_RETRY:-20}"
export GLOBAL_HEALTH_WAIT="${GLOBAL_HEALTH_WAIT:-30}"
export BETWEEN_NODES_WAIT="${BETWEEN_NODES_WAIT:-2}"
export MAX_ALLOWABLE_NODE_AGE="${MAX_ALLOWABLE_NODE_AGE:-10000}"
export K8S_AUTOSCALER_ENABLED="${K8S_AUTOSCALER_ENABLED:-true}"
export K8S_AUTOSCALER_NAMESPACE="${K8S_AUTOSCALER_NAMESPACE:-kube-system}"
export K8S_AUTOSCALER_DEPLOYMENT="${K8S_AUTOSCALER_DEPLOYMENT:-cluster-autoscaler-aws-cluster-autoscaler}"
export EXCLUDE_NODE_LABEL_KEYS="${EXCLUDE_NODE_LABEL_KEYS:-windows-version node.kubernetes.io/windows-build}"
#export EXCLUDE_NODE_LABEL_KEYS="${EXCLUDE_NODE_LABEL_KEYS:-node-lifecycle alpha.eksctl.io/instance-id}"

export CLUSTER="sandbox2-v2"
python ./eksrollup/dd-k8s.py --cluster_name $CLUSTER --plan

#echo -e "\e[0;33m********** Rolling $CLUSTER in $ENV_PREFIX-$ENVIRONMENT **********\e[0m"
#python3 ./eks_rolling_update.py --cluster_name $CLUSTER