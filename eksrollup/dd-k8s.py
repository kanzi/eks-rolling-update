import argparse
import datetime
import boto3
from kubernetes import client, config
from lib.logger import logger
from config import app_config
from lib.aws import is_asg_scaled, is_asg_healthy, instance_terminated, get_asg_tag, modify_aws_autoscaling, \
    count_all_cluster_instances, count_os_targeted_cluster_instances, save_asg_tags, get_asgs, get_all_asgs, get_os_targeted_asgs, scale_asg, plan_asgs, terminate_instance_in_asg, delete_asg_tags, plan_asgs_older_nodes, instance_outdated_age
from lib.k8s import k8s_nodes_count, k8s_nodes_ready, get_k8s_nodes, modify_k8s_autoscaler, get_node_by_instance_id, \
    drain_node, delete_node, cordon_node, taint_node
# from .lib.exceptions import RollingUpdateException


def get_node_os(k8s_node):
    labels = k8s_node.metadata.labels
    for label, value in labels.items():
        if label == "kubernetes.io/os":
            return value


def get_k8s_nodes_by_os(exclude_node_label_keys=app_config["EXCLUDE_NODE_LABEL_KEYS"]):
    """
    Returns list of nodes based on OS {node_name, node_os}
    """
    config.load_kube_config()

    k8s_api = client.CoreV1Api()
    logger.info("Getting k8s nodes ...")
    response = k8s_api.list_node()
    k8s_nodes = []
    for k8s_node in response.items:
        if all(key not in k8s_node.metadata.labels for key in exclude_node_label_keys):
            node_name = k8s_node.metadata.name
            node_os = get_node_os(k8s_node)
            k8s_nodes.append({'name': node_name, 'os': node_os})

    logger.info(f"Current total k8s node count is {len(response.items)} "
                f"(included: {len(k8s_nodes)} excluded: {len(response.items) - len(k8s_nodes)})")
    return k8s_nodes


def count_not_excluded_instances(cluster_name, predictive=False, exclude_node_label_keys=app_config["EXCLUDE_NODE_LABEL_KEYS"]):
    """
    Returns the number of ec2 instances in a k8s cluster excluding nodes with certain label keys
    """

    # Get the K8s nodes on the cluster, while excluding nodes with certain label keys
    k8s_nodes, excluded_k8s_nodes = get_k8s_nodes(exclude_node_label_keys)
    count = 0
    asgs = get_all_asgs(cluster_name)

    for asg in asgs:
        instances = asg['Instances']
        if predictive:
            count += asg['DesiredCapacity']
        else:
            # Use the get_node_by_instance_id() function as it only returns the node if it is not excluded by K8s labels
            for instance in instances:
                instance_id = instance['InstanceId']
                try:
                    get_node_by_instance_id(k8s_nodes, instance_id)
                    count += 1
                except Exception:
                    logger.info("Skipping instance {}".format(instance_id))
    logger.info("{} asg instance count in cluster is: {}. K8s node count should match this number".format("*** Predicted" if predictive else "Current", count))
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rolling update on cluster')
    parser.add_argument('--cluster_name', '-c', required=True,
                        help='the cluster name to perform rolling update on')
    parser.add_argument('--plan', '-p', action='store_const', const=True,
                        help='perform a dry run to see which instances are out of date')
    args = parser.parse_args()

    cluster_name = args.cluster_name
    nodes, excl_nodes = get_k8s_nodes()
    # print(80 * '-')
    # print(f"{'Node name':55}|  {'Node OS':25}")
    # print(80 * '-')
    for node in nodes:
        print(node.metadata.name)
        # print(f"{node['name']:55}|  {node['os']:25}")
        # logger.info(f"Node name: {node['name']}, Node OS: {node['os']}")
    # print(80 * '-')
    # filtered_asgs = get_asgs(cluster_name)
    # days_fresh = app_config['MAX_ALLOWABLE_NODE_AGE']
    # for filtered_asg in filtered_asgs:
    #     instances = filtered_asg['Instances']
    #     if instances:
    #         for instance in instances:
    #             instance_id = instance['InstanceId']
    #             instance_outdated_age(instance_id, days_fresh)

    run_mode = app_config['RUN_MODE']
    # perform a dry run on mode 4 for older nodes
    if (args.plan or app_config['DRY_RUN']) and (run_mode == 4):


        # all_asgs = get_asgs(cluster_name)
        # for asg in all_asgs:
        #     print(asg)

        targeted_asgs = get_os_targeted_asgs(cluster_name)
        # for targeted_asg in targeted_asgs:
        #     print(targeted_asg)


        # print(count_os_targeted_cluster_instances(cluster_name, predictive=True))


        # filtered_asgs = get_asgs(cluster_name)
        # for filtered_asg in filtered_asgs:
        #     print(filtered_asg)
        # print(80 * '=')
        # filtered_asgs = get_all_asgs(cluster_name)
        # for filtered_asg in filtered_asgs:
        #     print(filtered_asg)

        # outdated_nodes = plan_asgs_older_nodes(filtered_asgs)
        #
        # for asg_name, asg_tuple in outdated_nodes.items():
        #     outdated_instances, asg = asg_tuple
        #     outdated_instance_count = len(outdated_instances)
        #
        #     for outdated_instance in outdated_instances:
        #         outdated_instance_id = outdated_instance['InstanceId']
        #         get_node_by_instance_id(nodes, outdated_instance_id)


