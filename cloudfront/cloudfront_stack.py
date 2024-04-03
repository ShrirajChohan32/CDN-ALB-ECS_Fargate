from aws_cdk import (
    Duration,
    Environment,
    Stack,
    CfnOutput,
    aws_wafv2 as wafv2,
    aws_cloudfront as cloudfront,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_cloudfront_origins as origins,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ssm as ssm
)

import boto3
import time
# import json
# import yaml
# import re


from constructs import Construct
import aws_cdk as cdk
from aws_cdk.aws_ec2 import SubnetSelection, SubnetType
from aws_cdk.aws_ec2 import CfnNatGateway
from aws_cdk.aws_cloudfront import OriginProtocolPolicy
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationListenerRule
from aws_cdk.aws_cloudfront_origins import LoadBalancerV2Origin
app = cdk.App()
# from aws_cdk.aws_arn import AwsArn

import aws_cdk as cdk
from aws_cdk import Fn


class WAFStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the custom rules
        rate_limit_rule = wafv2.CfnWebACL.RuleProperty(
            name="Custom-RateLimit500",
            priority=0,
            action=wafv2.CfnWebACL.RuleActionProperty(block={}),
            statement=wafv2.CfnWebACL.StatementProperty(
                rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                    limit=500,
                    aggregate_key_type="IP"
                )
            ),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True,
                cloud_watch_metrics_enabled=True,
                metric_name="Custom-RateLimit500"
            )
        )
        managed_rule_1 = wafv2.CfnWebACL.RuleProperty(
            priority=1,
            override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
            statement=wafv2.CfnWebACL.StatementProperty(
                managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                    name="AWSManagedRulesBotControlRuleSet",
                    vendor_name="AWS"
                )
            ),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True,
                cloud_watch_metrics_enabled=True,
                metric_name="AWS-AWSManagedRulesBotControlRuleSet"
            ),
            name="AWS-AWSManagedRulesBotControlRuleSet"
        )
        # Define more managed rules and custom rules here as needed
        managed_rule_2 = wafv2.CfnWebACL.RuleProperty(
            priority=2,
            override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
            statement=wafv2.CfnWebACL.StatementProperty(
                managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                    name="AWSManagedRulesAmazonIpReputationList",
                    vendor_name="AWS"
                )
            ),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True,
                cloud_watch_metrics_enabled=True,
                metric_name="AWS-AWSManagedRulesAmazonIpReputationList"
            ),
            name="AWS-AWSManagedRulesAmazonIpReputationList"
        )

        managed_rule_3 = wafv2.CfnWebACL.RuleProperty(
            priority=3,
            override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
            statement=wafv2.CfnWebACL.StatementProperty(
                managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                    name="AWSManagedRulesCommonRuleSet",
                    vendor_name="AWS"
                )
            ),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True,
                cloud_watch_metrics_enabled=True,
                metric_name="AWS-AWSManagedRulesCommonRuleSet"
            ),
            name="AWS-AWSManagedRulesCommonRuleSet"
        )

        managed_rule_4 = wafv2.CfnWebACL.RuleProperty(
            priority=4,
            override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
            statement=wafv2.CfnWebACL.StatementProperty(
                managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                    name="AWSManagedRulesKnownBadInputsRuleSet",
                    vendor_name="AWS"
                )
            ),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True,
                cloud_watch_metrics_enabled=True,
                metric_name="AWS-AWSManagedRulesKnownBadInputsRuleSet"
            ),
            name="AWS-AWSManagedRulesKnownBadInputsRuleSet"
        )

        managed_rule_5 = wafv2.CfnWebACL.RuleProperty(
            priority=5,
            override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
            statement=wafv2.CfnWebACL.StatementProperty(
                managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                    name="AWSManagedRulesSQLiRuleSet",
                    vendor_name="AWS"
                )
            ),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True,
                cloud_watch_metrics_enabled=True,
                metric_name="AWS-AWSManagedRulesSQLiRuleSet"
            ),
            name="AWS-AWSManagedRulesSQLiRuleSet"
        )

        # AWS-AWSManagedRulesSQLiRuleSet

        self.web_acl_name = "DDOSACL" 

        # Create the web ACL and attach the rules to it
        self.web_acl = wafv2.CfnWebACL(
            self,
            "MyWebACL",
            name=self.web_acl_name,
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            scope="CLOUDFRONT",
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                sampled_requests_enabled=True,
                metric_name="MyWebACL"
            ),
            rules=[rate_limit_rule, managed_rule_1,managed_rule_2,managed_rule_3,managed_rule_4,managed_rule_5],
        )

        waf_arn_output = CfnOutput(self, 'WafArnOutput', value=self.web_acl.attr_arn, description='ARN of the WAF')



class CloudfrontResourceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # self.lb_name = self.alb() 
        self.lb_name = "Cloudfront-origin"

           # Create a VPC
        self.fargate_vpc = ec2.Vpc(self, "MyVpc",
            max_azs=2,ip_addresses=ec2.IpAddresses.cidr("10.4.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=28
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=28,
                    
                ),
            ],
        )

        # # Create a Cluster
        Fargate_cluster = ecs.Cluster(self, "FargateCluster",vpc=self.fargate_vpc,cluster_name="Fargate_CDK_Cluster")

        load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
            load_balancer_name=self.lb_name, cluster=Fargate_cluster,
            memory_limit_mib=1024, desired_count=1, cpu=512, 
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        )
            )

        fargate_load_balancer_arn= load_balanced_fargate_service.load_balancer.load_balancer_arn

        # Create an output to display the load balancer ARN
        load_balancer_arn_output = CfnOutput(
            self,
            'LoadBalancerArnOutput',
            value=fargate_load_balancer_arn,
            description='ARN of the load balancer'
        )



class CloudfrontStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, web_acl_name: str, lb_name: str, fargate_vpc , **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Us_east_1_web_acl_name = self.web_acl_name = web_acl_name
        # print(Us_east_1_web_acl_name)

        # Create a Boto3 client for the Elastic Load Balancing (ELB) service
        elbv2_client = boto3.client('elbv2')

        # Retrieve the ALB ARN using the load balancer name
        load_balancer_name = self.lb_name = lb_name
        response = elbv2_client.describe_load_balancers(Names=[load_balancer_name])

        # Extract the ALB ARN from the response
        alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']

        listener_info = elbv2_client.describe_listeners(LoadBalancerArn=alb_arn)

        # Extract the ARNs of the listeners from the response
        existing_listener_arn = [listener['ListenerArn'] for listener in listener_info['Listeners']]

        target_group_arns = []
        for listener in listener_info['Listeners']:
            default_actions = listener.get('DefaultActions', [])
            for action in default_actions:
                if action.get('TargetGroupArn'):
                    target_group_arns.append(action['TargetGroupArn'])

        # Convert the list of target group ARNs into a single string
        target_group_arn_string = ", ".join(target_group_arns)
        
        print(target_group_arn_string)

        # Convert the list into a string
        existing_listener_arn_string = ', '.join(existing_listener_arn)
        print(existing_listener_arn_string)

        alb = elbv2.ApplicationLoadBalancer.from_lookup( self,"ALB",
            load_balancer_arn=alb_arn)
        
        # Create a listener rule with the fixed response action
        listener_rule = elbv2.CfnListenerRule(
            self,
            "MyListenerRule",
            actions=[
                elbv2.CfnListenerRule.ActionProperty(
                    type="forward",
                    target_group_arn=target_group_arn_string
                )
            ],
            conditions=[
                elbv2.CfnListenerRule.RuleConditionProperty(
                    field="http-header",
                    http_header_config=elbv2.CfnListenerRule.HttpHeaderConfigProperty(
                        http_header_name="New",
                        values=["Zealand"]
                    )
                )
            ],
            listener_arn=existing_listener_arn_string,
            priority=1,
        ) 

                # Create the listener rule with the fixed response
        default_rule = elbv2.CfnListenerRule(
            self,
            "FixedResponseRule",
            actions=[
                elbv2.CfnListenerRule.ActionProperty(
                    type="fixed-response",
                    fixed_response_config=elbv2.CfnListenerRule.FixedResponseConfigProperty(
                        status_code="403",
                        message_body="Forbidden"
                    )
                )
            ],
            conditions=[
                elbv2.CfnListenerRule.RuleConditionProperty(
                    field="path-pattern",
                    path_pattern_config=elbv2.CfnListenerRule.PathPatternConfigProperty(
                        values=["/*"]
                    )
                )
            ],
            listener_arn=existing_listener_arn_string,
            priority=2,
        )

        # # The Below SDk gets the default listener rule 

        # modifyOnBeta = elbv2_client.modify_listener(
        #     ListenerArn=existing_listener_arn_string,
        #     DefaultActions=[
        #         {
        #             'Type': 'fixed-response',
        #             'FixedResponseConfig': {
        #                 'StatusCode': '403',
        #                 'ContentType': 'text/plain',
        #                 'MessageBody': 'SORRY UNREACHABLE'
        #             }
        #         }
        #     ]
        # )

        # ##### Alternatively use the above SDK works to modify the Default listener rule

                # Create a Boto3 WAFV2 client
        wafv2_client = boto3.client('wafv2',region_name='us-east-1')

        # Provide the ARN of the CloudFront distribution
        response = wafv2_client.list_web_acls(Scope='CLOUDFRONT')

        # Extract the list of Web ACLs from the response
        web_acls = response['WebACLs']

        for web_acl in web_acls:
            # web_acl_id = web_acl['Id']
            web_acl_name = web_acl['Name']
            if web_acl_name == Us_east_1_web_acl_name:
                web_acl_arn = web_acl['ARN']
            else:
                print("Web ACL not found")
        # print(web_acl_arn)
        
        # Create the CloudFront distribution
        CDN = cloudfront.Distribution(
            self,
            "myDist",
            web_acl_id=web_acl_arn,
            default_behavior=cloudfront.BehaviorOptions(
                origin=LoadBalancerV2Origin(
                    load_balancer=alb,
                    protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                    custom_headers={"New": "Zealand"}
                ),
            ),
        )
        
        ##########

        # Us_east_1_web_acl_name = self.web_acl_name = web_acl_name

        # # # print(f"Web ACL Name in CloudfrontResourceStack: {Us_east_1_web_acl_name}")

        # # Create a Boto3 client for the Elastic Load Balancing (ELB) service
        # elbv2_client = boto3.client('elbv2')

        # # Retrieve the ALB ARN using the load balancer name
        # load_balancer_name = self.lb_name = lb_name
        # response = elbv2_client.describe_load_balancers(Names=[load_balancer_name])

        # # print(f"LB ARN", response)

        # # Extract the ALB ARN from the response
        # alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']

        # # Retrieve all target groups
        # target_group_info = elbv2_client.describe_target_groups()
        # # print(target_group_info)

        # # Extract the ARNs of the target groups from the response
        # existing_target_group_arn = [target_group['TargetGroupArn'] for target_group in target_group_info['TargetGroups']]

        # # Convert the list into a string
        # target_group_arn_string = ', '.join(existing_target_group_arn)
        # print(f"TArrget gourps",target_group_arn_string)

        # listener_info = elbv2_client.describe_listeners(LoadBalancerArn=alb_arn)

        # # Extract the ARNs of the listeners from the response
        # existing_listener_arn = [listener['ListenerArn'] for listener in listener_info['Listeners']]

        # # Convert the list into a string
        # existing_listener_arn_string = ', '.join(existing_listener_arn)
        # # print(existing_listener_arn_string)

        # alb = elbv2.ApplicationLoadBalancer.from_lookup( self,"ALB",
        #     load_balancer_arn=alb_arn)


        # # listener_rule = elbv2.ApplicationListenerRule(self, "MyListenerRule",
        # #     action=elbv2.ListenerAction.forward(
        # #     target_groups=[target_group_arn_string]),
        # #     conditions=[elbv2.ListenerCondition.http_header("New", ["Zealand"])],
        # #     listener_arn=existing_listener_arn_string,
        # #     listener=alb.add_listener("Listener", port=80),
        # #     priority=1,
        
        # # Create a listener rule with the fixed response action
        # listener_rule = elbv2.CfnListenerRule(
        #     self,
        #     "MyListenerRule",
        #     actions=[
        #         elbv2.CfnListenerRule.ActionProperty(
        #             type="forward",
        #             target_group_arn=target_group_arn_string
        #         )
        #     ],
        #     conditions=[
        #         elbv2.CfnListenerRule.RuleConditionProperty(
        #             field="http-header",
        #             http_header_config=elbv2.CfnListenerRule.HttpHeaderConfigProperty(
        #                 http_header_name="New",
        #                 values=["Zealand"]
        #             )
        #         )
        #     ],
        #     listener_arn=existing_listener_arn_string,
        #     priority=1,
        # ) 


        # # listener_rule = elbv2.CfnListenerRule(
        # #     self,
        # #     "MyListenerRule",
        # #     actions=[
        # #         elbv2.CfnListenerRule.ActionProperty(
        # #             type="forward",
        # #             target_group_arn=target_group_arn_string
        # #         )
        # #     ],
        # #     conditions=[
        # #         elbv2.CfnListenerRule.RuleConditionProperty(
        # #             field="http-header",
        # #             http_header_config=elbv2.CfnListenerRule.HttpHeaderConfigProperty(
        # #                 http_header_name="New",
        # #                 values=["Zealand"]
        # #             )
        # #         )
        # #     ],
        # #     listener_arn=existing_listener_arn_string,
        # #     priority=1,



        # #         # Create the listener rule with the fixed response
        # # default_rule = elbv2.CfnListenerRule(
        # #     self,
        # #     "FixedResponseRule",
        # #     actions=[
        # #         elbv2.CfnListenerRule.ActionProperty(
        # #             type="fixed-response",
        # #             fixed_response_config=elbv2.CfnListenerRule.FixedResponseConfigProperty(
        # #                 status_code="403",
        # #                 message_body="Forbidden"
        # #             )
        # #         )
        # #     ],
        # #     conditions=[
        # #         elbv2.CfnListenerRule.RuleConditionProperty(
        # #             field="path-pattern",
        # #             path_pattern_config=elbv2.CfnListenerRule.PathPatternConfigProperty(
        # #                 values=["/*"]
        # #             )
        # #         )
        # #     ],
        # #     listener_arn=existing_listener_arn_string,
        # #     priority=2,
        # # )

        # # # The Below SDk gets the default listener rule 

        # modifyOnBeta = elbv2_client.modify_listener(
        #     ListenerArn=existing_listener_arn_string,
        #     DefaultActions=[
        #         {
        #             'Type': 'fixed-response',
        #             'FixedResponseConfig': {
        #                 'StatusCode': '403',
        #                 'ContentType': 'text/plain',
        #                 'MessageBody': 'SORRY UNREACHABLE'
        #             }
        #         }
        #     ]
        # )

        # # #####This aboce SDK works






        #         # Create a Boto3 WAFV2 client
        # wafv2_client = boto3.client('wafv2',region_name='us-east-1')

        # # Provide the ARN of the CloudFront distribution
        # response = wafv2_client.list_web_acls(Scope='CLOUDFRONT')

        # # Extract the list of Web ACLs from the response
        # web_acls = response['WebACLs']

        # for web_acl in web_acls:
        #     # web_acl_id = web_acl['Id']
        #     web_acl_name = web_acl['Name']
        #     if web_acl_name == Us_east_1_web_acl_name:
        #         web_acl_arn = web_acl['ARN']
        # # print(web_acl_arn)

   
        
        # # Create the CloudFront distribution
        # CDN = cloudfront.Distribution(
        #     self,
        #     "myDist",
        #     web_acl_id=web_acl_arn,
        #     default_behavior=cloudfront.BehaviorOptions(
        #         origin=LoadBalancerV2Origin(
        #             load_balancer=alb,
        #             protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
        #             custom_headers={"New": "Zealand"}
        #         ),
        #     ),
        # )