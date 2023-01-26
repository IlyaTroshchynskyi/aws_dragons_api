import os
import json
print('*************************************************************************************************')
# res = os.system('sam local invoke "DragonFunction" -e ./events/data.json  --template-file ./template.yaml --env-vars ./env.json  --docker-network dragons' )
# print(res)
res2 = os.popen('sam local invoke "DragonFunction" -e ./events/data.json  --template-file ./template.yaml --env-vars ./env.json  --docker-network dragons' )
print(type(res2))
print()
print(f'=={res2.read()}')
# print(json.loads(res))

import boto3
import botocore

# Set "running_locally" flag if you are running the integration test locally
# running_locally = True

# if running_locally:
#
#     # Create Lambda SDK client to connect to appropriate Lambda endpoint
#     lambda_client = boto3.client('lambda',
#         region_name="us-east-q",
#         endpoint_url="http://127.0.0.1:3000",
#         use_ssl=False,
#         verify=False,
#         # config=botocore.client.Config(
#         #     signature_version=botocore.UNSIGNED,
#         #     read_timeout=1,
#         #     retries={'max_attempts': 0},
#         # )
#     )
#     print('============================')
# else:
#     lambda_client = boto3.client('lambda')


# Invoke your Lambda function as you normally usually do. The function will run
# locally if it is configured to do so
# response = lambda_client.invoke(FunctionName="DragonFunction")
# print(response)