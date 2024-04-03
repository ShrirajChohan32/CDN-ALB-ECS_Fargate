#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cloudfront.cloudfront_stack import WAFStack
from cloudfront.cloudfront_stack import CloudfrontResourceStack
from cloudfront.cloudfront_stack import CloudfrontStack




app = cdk.App()

syd_env=cdk.Environment(account="12345678907",region="ap-southeast-2")
us_env=cdk.Environment(region="us-east-1")

waf_stack = WAFStack(app, "WAFStack",env = us_env)
resource_stack = CloudfrontResourceStack(app,"ResourceStack", env=syd_env)
CDN_Stack = CloudfrontStack(app,"CDNStack", env=syd_env,web_acl_name=waf_stack.web_acl_name,lb_name=resource_stack.lb_name, fargate_vpc=resource_stack.fargate_vpc)

app.synth()



