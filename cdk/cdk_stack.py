from aws_cdk import (
    aws_iot as iot,
    aws_greengrass as gg,
    core
)
import boto3_helper

class CdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # create iot thing & policy
        gg_core = iot.CfnThing(self,
            'MyGGGCDKCore',
            thing_name='myggg-core'
        )
        print('## Thing Name: %s' % gg_core.thing_name)

        thing_policy = iot.CfnPolicy(self,
            'MyGGGCDKCorePolicy',
            policy_document=boto3_helper.policyDocument,
            policy_name='myggg-core-policy'
        )
        print('## Policy Name: %s' % thing_policy.policy_name)

        thing_policy = iot.CfnPolicy(self,
            'MyGGGCDKGroupPolicy',
            policy_document=boto3_helper.policyDocument,
            policy_name='myggg-group-policy'
        )      

        # create greengrass group
        ggg = gg.CfnGroup(self,
            'MyGGGCDKGroup',
            name='myggg-name'
            #role_arn='myggg-role'  # optional
        )

        # gg_device_def = gg.CfnDeviceDefinition(self,
        #     'MyGGGCDKDeviceDefinition',
        #     name='myggg-device-definition'
        # )




        '''TODO'''
        # add gg_core to core definition (check in console)
        # add core definition to group ""
        # try aws cli to understand logical order of core definition

        # create iot thing certificate
        certArn = boto3_helper.create_csr()  # ugh! - gens a new cert for each deployment
        thing_policy_principal_props = iot.CfnPolicyPrincipalAttachmentProps(
            policy_name=thing_policy.policy_name,
            principal=certArn
        )
        print('## Principal Cert Arn: %s' % thing_policy_principal_props.principal)


        gg_core_def = gg.CfnCoreDefinition(self,
            'MyGGGCDKCoreDefinition',
            name='myggg-core-definition',
            initial_version=1
        )

        gg_core_def_version = gg.CfnCoreDefinitionVersion(self,
            'MyGGCDKCoreDefinitionVersion',
            core_definition_id=gg_core_def.logical_id,
            cores=[
                {
                    "id": "blah",
                    "thingArn": gg_core.get_att.thingArn,
                    "certificateArn": "blah",
                    "syncShadow": True
                }
            ]
        )


        # attach policy to iot certificate
        iot.CfnPolicyPrincipalAttachment(self,
            'MyGGGCDKPolicyPrincipalAttachment',
            policy_name=thing_policy.policy_name,
            principal=thing_policy_principal_props.principal
        ).add_depends_on(
            resource=gg_core
        )

        # attach certificate to iot thing
        iot.CfnThingPrincipalAttachment(self,
            'MyGGGCDKThingPrincipalAttachment',
            thing_name=gg_core.thing_name,
            principal=thing_policy_principal_props.principal
        ).add_depends_on(
            resource=gg_core
        )