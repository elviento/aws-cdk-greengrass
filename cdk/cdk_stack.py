from aws_cdk import (
    aws_iot as iot,
    aws_greengrass as gg,
    core
)
import boto3_helper

class CdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # JITP new device certificate
        # https://aws.amazon.com/blogs/iot/setting-up-just-in-time-provisioning-with-aws-iot-core/
        # mosquitto_pub --cafile root.cert --cert deviceCertAndCACert.crt --key deviceCert.key -h <prefix>.iot.us-east-1.amazonaws.com -p 8883 -q 1 -t foo/bar -I xyz --tls-version tlsv1.2 -m "Hello" -d
        certArn = 'arn:aws:iot:us-east-1:1234567890:cert/xyz'
        region = core.Stack.of(self).region
        accountId = core.Stack.of(self).account
        print('region: %s' % region)


        ## IOT THING BEGIN ##

        # create iot thing
        gg_core = iot.CfnThing(self,
            'MyGGGCDKCore',
            thing_name='myggg-core'
        )
        coreArn = 'arn:aws:iot:%s:%s:thing/%s' % (region, accountId, gg_core.thing_name)
        print('## Thing Name: %s' % gg_core.thing_name)

        # create iot policy
        thing_policy = iot.CfnPolicy(self,
            'MyGGGCDKCorePolicy',
            policy_document=boto3_helper.policyDocument,
            policy_name='myggg-core-policy'
        )
        print('## Policy Name: %s' % thing_policy.policy_name)   


        # create iot thing certificate
        # uncomment boto3_helper.create_csr() if you want to use AWS keys and certs
        #certArn = boto3_helper.create_csr()  # ugh! - gens a new cert for each deployment

        # using a self-signed cacert csr
        # cacert_csr=boto3_helper.read_csr()
        # iot_cacert = iot.CfnCertificate(self,
        #     'MyGGGCDKCACertificate',
        #     certificate_signing_request=cacert_csr,
        #     status="ACTIVE"
        # )
        # certArn=iot_cacert.attr_arn
        # print('## Show me Cert ARN: %s' % iot_cacert.attr_arn)

        # attach policy to principal cert
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

        ## IOT THING END ##

        ## GREENGRASS BEGIN ##

        # Configure Greengrass Group & Associate IoT Thing to Greengrass Core

        # core definition version
        core_version_details = [{
            'id': '1',
            'certificateArn': certArn,
            'thingArn': coreArn,
            'shadowSync': True
        }]

        gg_core_def = gg.CfnCoreDefinition(self, 'MyGGGCDKCoreDefinition',
            name='Raspberry_Pi_Core',
            initial_version={ 'cores': core_version_details }
        )
        gg_core_def.add_depends_on(gg_core)

        gg_core_def_version = gg.CfnCoreDefinitionVersion(self,
            'MyGGCDKCoreDefinitionVersion',
            core_definition_id=gg_core_def.attr_id,
            cores=core_version_details
        )

        # create greengrass group
        gg_group = gg.CfnGroup(self,
            'MyGGGCDKGroup',
            name='myggg-name',
            initial_version={
                'coreDefinitionVersionArn': gg_core_def.attr_latest_version_arn
            }
        )
        gg_group.add_depends_on(gg_core_def)

        # external ref: https://translate.google.com/translate?depth=1&hl=en&nv=1&rurl=translate.google.com&sl=auto&sp=nmt4&tl=en&u=https://dev.classmethod.jp/cloud/aws/aws-cdk-greengrass-rasberrypi/&xid=17259,15700002,15700023,15700186,15700191,15700256,15700259,15700262,15700265,15700271
        ## GREENGRASS END ##