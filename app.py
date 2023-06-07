#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloudfront.cloudfront_stack import WAFStack
from cloudfront.cloudfront_stack import CloudfrontResourceStack
from cloudfront.cloudfront_stack import CloudfrontStack




app = cdk.App()

syd_env=cdk.Environment(account="273541776559",region="ap-southeast-2")


# cloudfront_stack = CloudfrontStack(app, "CloudFrontStack", env={'region': 'us-east-1'})

# # resources = CloudfrontResourceStack(app,"ResourceStack", env={'region': 'ap-southeast-2'})

us_env=cdk.Environment(account="273541776559",region="us-east-1")

waf_stack = WAFStack(app, "WAFStack",env = us_env)
# CloudfrontResourceStack(app,"ResourceStack", env=syd_env,web_acl_name=cloudfront_stack.web_acl_name)
resource_stack = CloudfrontResourceStack(app,"ResourceStack", env=syd_env)
CDN_Stack = CloudfrontStack(app,"CDNStack", env=syd_env,web_acl_name=waf_stack.web_acl_name,lb_name=resource_stack.lb_name, fargate_vpc=resource_stack.fargate_vpc)



    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

# env=cdk.Environment(account=os.getenv('273541776559'), region=os.getenv('ap-southeast-2')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    # )

app.synth()
