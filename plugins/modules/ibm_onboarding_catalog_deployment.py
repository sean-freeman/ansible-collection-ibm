#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_onboarding_catalog_deployment
for_more_info:  refer - https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs/resources/onboarding_catalog_deployment

short_description: Configure IBM Cloud 'ibm_onboarding_catalog_deployment' resource

version_added: "2.8"

description:
    - Create, update or destroy an IBM Cloud 'ibm_onboarding_catalog_deployment' resource
    - This module does not support idempotency
requirements:
    - IBM-Cloud terraform-provider-ibm v1.71.2
    - Terraform v1.5.5

options:
    catalog_plan_id:
        description:
            - (Required for new resource) The unique ID of this global catalog plan.
        required: True
        type: str
    product_id:
        description:
            - (Required for new resource) The unique ID of the product.
        required: True
        type: str
    name:
        description:
            - (Required for new resource) The programmatic name of this deployment.
        required: True
        type: str
    kind:
        description:
            - (Required for new resource) The kind of the global catalog object.
        required: True
        type: str
    env:
        description:
            - The environment to fetch this object from.
        required: False
        type: str
    active:
        description:
            - (Required for new resource) Whether the service is active.
        required: True
        type: bool
    disabled:
        description:
            - (Required for new resource) Determines the global visibility for the catalog entry, and its children. If it is not enabled, all plans are disabled.
        required: True
        type: bool
    overview_ui:
        description:
            - The object that contains the service details from the Overview page in global catalog.
        required: False
        type: list
        elements: dict
    object_provider:
        description:
            - (Required for new resource) The provider or owner of the product.
        required: True
        type: list
        elements: dict
    catalog_product_id:
        description:
            - (Required for new resource) The unique ID of this global catalog product.
        required: True
        type: str
    object_id:
        description:
            - The desired ID of the global catalog object.
        required: False
        type: str
    tags:
        description:
            - (Required for new resource) A list of tags that carry information about your product. These tags can be used to find your product in the IBM Cloud catalog.
        required: True
        type: list
        elements: str
    metadata:
        description:
            - Global catalog deployment metadata.
        required: False
        type: list
        elements: dict
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
            - The IBM Cloud Classic Infrastructure (SoftLayer) user name. This
              can also be provided via the environment variable
              'IAAS_CLASSIC_USERNAME'.
        required: False
    iaas_classic_api_key:
        description:
            - The IBM Cloud Classic Infrastructure API key. This can also be
              provided via the environment variable 'IAAS_CLASSIC_API_KEY'.
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
    ('catalog_plan_id', 'str'),
    ('product_id', 'str'),
    ('name', 'str'),
    ('kind', 'str'),
    ('active', 'bool'),
    ('disabled', 'bool'),
    ('object_provider', 'list'),
    ('catalog_product_id', 'str'),
    ('tags', 'list'),
]

# All top level parameter keys supported by Terraform module
TL_ALL_PARAMETERS = [
    'catalog_plan_id',
    'product_id',
    'name',
    'kind',
    'env',
    'active',
    'disabled',
    'overview_ui',
    'object_provider',
    'catalog_product_id',
    'object_id',
    'tags',
    'metadata',
]

# Params for Data source
TL_REQUIRED_PARAMETERS_DS = [
]

TL_ALL_PARAMETERS_DS = [
]

TL_CONFLICTS_MAP = {
}

# define available arguments/parameters a user can pass to the module
from ansible_collections.ibm.cloudcollection.plugins.module_utils.ibmcloud import Terraform, ibmcloud_terraform
from ansible.module_utils.basic import env_fallback
module_args = dict(
    catalog_plan_id=dict(
        required=False,
        type='str'),
    product_id=dict(
        required=False,
        type='str'),
    name=dict(
        required=False,
        type='str'),
    kind=dict(
        required=False,
        type='str'),
    env=dict(
        required=False,
        type='str'),
    active=dict(
        required=False,
        type='bool'),
    disabled=dict(
        required=False,
        type='bool'),
    overview_ui=dict(
        required=False,
        elements='',
        type='list'),
    object_provider=dict(
        required=False,
        elements='',
        type='list'),
    catalog_product_id=dict(
        required=False,
        type='str'),
    object_id=dict(
        required=False,
        type='str'),
    tags=dict(
        required=False,
        elements='',
        type='list'),
    metadata=dict(
        required=False,
        elements='',
        type='list'),
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

    result = ibmcloud_terraform(
        resource_type='ibm_onboarding_catalog_deployment',
        tf_type='resource',
        parameters=module.params,
        ibm_provider_version='1.71.2',
        tl_required_params=TL_REQUIRED_PARAMETERS,
        tl_all_params=TL_ALL_PARAMETERS)

    if result['rc'] > 0:
        module.fail_json(
            msg=Terraform.parse_stderr(result['stderr']), **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()