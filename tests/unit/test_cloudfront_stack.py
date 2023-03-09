import aws_cdk as core
import aws_cdk.assertions as assertions

from cloudfront.cloudfront_stack import CloudfrontStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloudfront/cloudfront_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CloudfrontStack(app, "cloudfront")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
