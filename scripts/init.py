#!/usr/env/bin python

from cloudify import ctx
from cloudify.state import ctx_parameters

resource_prefix = ctx_parameters['resource_prefix']
env_type = ctx_parameters['env_type']

if env_type == 'dev':
    k8s_blueprint_id = 'minikube'
    k8s_inputs = {}
    db_blueprint_id = 'vm_with_psql'
    db_inputs = {}
elif env_type == 'production':
    k8s_blueprint_id = 'eks'
    k8s_inputs = {
        'eks_cluster_name': '{}cluster'.format(resource_prefix),
        'eks_nodegroup_name': '{}nodegroup'.format(resource_prefix),
        'service_account_name': 'app-user',
        'service_account_namespace': 'default'
    }
    db_blueprint_id = 'rds_psql'
    db_inputs = {
        "db_name": "{}rdsdb".format(resource_prefix)
    }
else:
    raise Exception("Unhandled environment type: {}".format(env_type))

ctx.instance.runtime_properties.update(
    {
        'k8s_blueprint_id': k8s_blueprint_id,
        'k8s_inputs': k8s_inputs,
        'db_blueprint_id': db_blueprint_id,
        'db_inputs': db_inputs
    })
