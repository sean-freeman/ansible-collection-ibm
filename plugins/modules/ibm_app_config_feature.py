#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_app_config_feature
for_more_info:  refer - https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs/resources/app_config_feature

short_description: Configure IBM Cloud 'ibm_app_config_feature' resource

version_added: "2.8"

description:
    - Create, update or destroy an IBM Cloud 'ibm_app_config_feature' resource
    - This module supports idempotency
requirements:
    - IBM-Cloud terraform-provider-ibm v1.27.0
    - Terraform v0.12.20

options:
    tags:
        description:
            - Tags associated with the feature.
        required: False
        type: str
    collections:
        description:
            - List of collection id representing the collections that are associated with the specified feature flag.
        required: False
        type: list
        elements: dict
    name:
        description:
            - (Required for new resource) Feature name.
        required: True
        type: str
    disabled_value:
        description:
            - (Required for new resource) Value of the feature when it is disabled. The value can be BOOLEAN, STRING or a NUMERIC value as per the `type` attribute.
        required: True
        type: str
    environment_id:
        description:
            - (Required for new resource) Environment Id.
        required: True
        type: str
    type:
        description:
            - (Required for new resource) Type of the feature (BOOLEAN, STRING, NUMERIC).
        required: True
        type: str
    segment_rules:
        description:
            - Specify the targeting rules that is used to set different feature flag values for different segments.
        required: False
        type: list
        elements: dict
    enabled_value:
        description:
            - (Required for new resource) Value of the feature when it is enabled. The value can be BOOLEAN, STRING or a NUMERIC value as per the `type` attribute.
        required: True
        type: str
    description:
        description:
            - Feature description.
        required: False
        type: str
    guid:
        description:
            - (Required for new resource) GUID of the App Configuration service. Get it from the service instance credentials section of the dashboard.
        required: True
        type: str
    feature_id:
        description:
            - (Required for new resource) Feature id.
        required: True
        type: str
    id:
        description:
            - (Required when updating or destroying existing resource) IBM Cloud Resource ID.
        required: False
        type: str
    state:
        description:
            - State of resource
        choices:
            - available
            - absent
        default: available
        required: False
    iaas_classic_username:
        description:
            - (Required when generation = 1) The IBM Cloud Classic
              Infrastructure (SoftLayer) user name. This can also be provided
              via the environment variable 'IAAS_CLASSIC_USERNAME'.
        required: False
    iaas_classic_api_key:
        description:
            - (Required when generation = 1) The IBM Cloud Classic
              Infrastructure API key. This can also be provided via the
              environment variable 'IAAS_CLASSIC_API_KEY'.
        required: False
    region:
        description:
            - The IBM Cloud region where you want to create your
              resources. If this value is not specified, us-south is
              used by default. This can also be provided via the
              environment variable 'IC_REGION'.
        default: us-south
        required: False
    ibmcloud_api_key:
        description:
            - The IBM Cloud API key to authenticate with the IBM Cloud
              platform. This can also be provided via the environment
              variable 'IC_API_KEY'.
        required: True

author:
    - Jay Carman (@jaywcarman)
'''

# Top level parameter keys required by Terraform module
TL_REQUIRED_PARAMETERS = [
    ('name', 'str'),
    ('disabled_value', 'str'),
    ('environment_id', 'str'),
    ('type', 'str'),
    ('enabled_value', 'str'),
    ('guid', 'str'),
    ('feature_id', 'str'),
]

# All top level parameter keys supported by Terraform module
TL_ALL_PARAMETERS = [
    'tags',
    'collections',
    'name',
    'disabled_value',
    'environment_id',
    'type',
    'segment_rules',
    'enabled_value',
    'description',
    'guid',
    'feature_id',
]

# Params for Data source
TL_REQUIRED_PARAMETERS_DS = [
    ('guid', 'str'),
    ('feature_id', 'str'),
    ('environment_id', 'str'),
]

TL_ALL_PARAMETERS_DS = [
    'includes',
    'guid',
    'feature_id',
    'environment_id',
]

TL_CONFLICTS_MAP = {
}

# define available arguments/parameters a user can pass to the module
from ansible_collections.ibm.cloudcollection.plugins.module_utils.ibmcloud import Terraform, ibmcloud_terraform
from ansible.module_utils.basic import env_fallback
module_args = dict(
    tags=dict(
        required=False,
        type='str'),
    collections=dict(
        required=False,
        elements='',
        type='list'),
    name=dict(
        required=False,
        type='str'),
    disabled_value=dict(
        required=False,
        type='str'),
    environment_id=dict(
        required=False,
        type='str'),
    type=dict(
        required=False,
        type='str'),
    segment_rules=dict(
        required=False,
        elements='',
        type='list'),
    enabled_value=dict(
        required=False,
        type='str'),
    description=dict(
        required=False,
        type='str'),
    guid=dict(
        required=False,
        type='str'),
    feature_id=dict(
        required=False,
        type='str'),
    id=dict(
        required=False,
        type='str'),
    state=dict(
        type='str',
        required=False,
        default='available',
        choices=(['available', 'absent'])),
    iaas_classic_username=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IAAS_CLASSIC_USERNAME']),
        required=False),
    iaas_classic_api_key=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IAAS_CLASSIC_API_KEY']),
        required=False),
    region=dict(
        type='str',
        fallback=(env_fallback, ['IC_REGION']),
        default='us-south'),
    ibmcloud_api_key=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IC_API_KEY']),
        required=True)
)


def run_module():
    from ansible.module_utils.basic import AnsibleModule

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # New resource required arguments checks
    missing_args = []
    if module.params['id'] is None:
        for arg, _ in TL_REQUIRED_PARAMETERS:
            if module.params[arg] is None:
                missing_args.append(arg)
        if missing_args:
            module.fail_json(msg=(
                "missing required arguments: " + ", ".join(missing_args)))

    conflicts = {}
    if len(TL_CONFLICTS_MAP) != 0:
        for arg in TL_CONFLICTS_MAP:
            if module.params[arg]:
                for conflict in TL_CONFLICTS_MAP[arg]:
                    try:
                        if module.params[conflict]:
                            conflicts[arg] = conflict
                    except KeyError:
                        pass
    if len(conflicts):
        module.fail_json(msg=("conflicts exist: {}".format(conflicts)))

    result_ds = ibmcloud_terraform(
        resource_type='ibm_app_config_feature',
        tf_type='data',
        parameters=module.params,
        ibm_provider_version='1.27.0',
        tl_required_params=TL_REQUIRED_PARAMETERS_DS,
        tl_all_params=TL_ALL_PARAMETERS_DS)

    if result_ds['rc'] != 0 or (result_ds['rc'] == 0 and (module.params['id'] is not None or module.params['state'] == 'absent')):
        result = ibmcloud_terraform(
            resource_type='ibm_app_config_feature',
            tf_type='resource',
            parameters=module.params,
            ibm_provider_version='1.27.0',
            tl_required_params=TL_REQUIRED_PARAMETERS,
            tl_all_params=TL_ALL_PARAMETERS)
        if result['rc'] > 0:
            module.fail_json(
                msg=Terraform.parse_stderr(result['stderr']), **result)

        module.exit_json(**result)
    else:
        module.exit_json(**result_ds)


def main():
    run_module()


if __name__ == '__main__':
    main()