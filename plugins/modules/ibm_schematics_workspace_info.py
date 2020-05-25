#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_schematics_workspace_info
short_description: Retrieve IBM Cloud 'ibm_schematics_workspace' resource

version_added: "2.8"

description:
    - Retrieve an IBM Cloud 'ibm_schematics_workspace' resource

requirements:
    - IBM-Cloud terraform-provider-ibm v1.6.0
    - Terraform v0.12.20

options:
    description:
        description:
            - The description of workspace
        required: False
        type: str
    resource_controller_url:
        description:
            - The URL of the IBM Cloud dashboard that can be used to explore and view details about this workspace
        required: False
        type: str
    name:
        description:
            - The name of workspace
        required: False
        type: str
    status:
        description:
            - The status of workspace
        required: False
        type: str
    tags:
        description:
            - None
        required: False
        type: list
        elements: str
    is_frozen:
        description:
            - None
        required: False
        type: bool
    is_locked:
        description:
            - None
        required: False
        type: bool
    crn:
        description:
            - cloud resource name of the workspace
        required: False
        type: str
    resource_group:
        description:
            - The resource group of workspace
        required: False
        type: str
    location:
        description:
            - The location of workspace
        required: False
        type: str
    catalog_ref:
        description:
            - Catalog references
        required: False
        type: dict
        elements: dict
    workspace_id:
        description:
            - The id of workspace
        required: True
        type: str
    template_id:
        description:
            - The id of templates
        required: False
        type: list
        elements: str
    types:
        description:
            - None
        required: False
        type: list
        elements: str
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
    ('workspace_id', 'str'),
]

# All top level parameter keys supported by Terraform module
TL_ALL_PARAMETERS = [
    'description',
    'resource_controller_url',
    'name',
    'status',
    'tags',
    'is_frozen',
    'is_locked',
    'crn',
    'resource_group',
    'location',
    'catalog_ref',
    'workspace_id',
    'template_id',
    'types',
]

# define available arguments/parameters a user can pass to the module
from ansible_collections.ibmcloud.ibmcollection.plugins.module_utils.ibmcloud import Terraform, ibmcloud_terraform
from ansible.module_utils.basic import env_fallback
module_args = dict(
    description=dict(
        required=False,
        type='str'),
    resource_controller_url=dict(
        required=False,
        type='str'),
    name=dict(
        required=False,
        type='str'),
    status=dict(
        required=False,
        type='str'),
    tags=dict(
        required=False,
        elements='',
        type='list'),
    is_frozen=dict(
        required=False,
        type='bool'),
    is_locked=dict(
        required=False,
        type='bool'),
    crn=dict(
        required=False,
        type='str'),
    resource_group=dict(
        required=False,
        type='str'),
    location=dict(
        required=False,
        type='str'),
    catalog_ref=dict(
        required=False,
        elements='',
        type='dict'),
    workspace_id=dict(
        required=True,
        type='str'),
    template_id=dict(
        required=False,
        elements='',
        type='list'),
    types=dict(
        required=False,
        elements='',
        type='list'),
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

    result = ibmcloud_terraform(
        resource_type='ibm_schematics_workspace',
        tf_type='data',
        parameters=module.params,
        ibm_provider_version='1.6.0',
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