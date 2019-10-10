from aws_cdk import (
    aws_iot as iot,
    core
)
import boto3_helper

class CdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # create iot thing & policy
        thing = iot.CfnThing(self,
            'MyGGGCDKThing',
            thing_name='myggg-core'
        )
        print('## Thing Name: %s' % thing.thing_name)

        thing_policy = iot.CfnPolicy(self,
            'MyGGGCDKThingPolicy',
            policy_document=boto3_helper.policyDocument,
            policy_name='myggg-policy'
        )

        # debug - get policy name 
        thing_policy_name = thing_policy.policy_name
        print('## Policy Name: %s' % thing_policy_name)

        # create iot thing certificate
        certArn = boto3_helper.create_csr()  # ugh! - gens a new cert for each deployment
        thing_policy_principal_props = iot.CfnPolicyPrincipalAttachmentProps(
            policy_name=thing_policy.policy_name,
            principal=certArn
        )
        print('## Principal Cert Arn: %s' % thing_policy_principal_props.principal)

        # attach policy to iot certificate
        iot.CfnPolicyPrincipalAttachment(self,
            'MyGGGCDKPolicyPrincipalAttachment',
            policy_name=thing_policy.policy_name,
            principal=thing_policy_principal_props.principal
        ).add_depends_on(
            resource=thing
        )

        # attach certificate to iot thing
        iot.CfnThingPrincipalAttachment(self,
            'MyGGGCDKThingPrincipalAttachment',
            thing_name=thing.thing_name,
            principal=thing_policy_principal_props.principal
        ).add_depends_on(
            resource=thing
        )