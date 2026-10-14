"""Lesson 10 lab C: a tiny POLICY CHECKER, run on the policies from the notebook. Simplified AWS-style rules, written for this lesson (not the real AWS engine).

Rules used: everything is denied unless a statement ALLOWS it; an explicit DENY always wins; '*' matches any characters; a deny with a Region condition
applies when the request's Region is not in the list (the organisation policy from the notebook).
We test 12 requests against a NARROW role (the notebook's example) and a BROAD role ('bedrock:*' on '*'). Run: python3 l10_iam_check.py
"""
from fnmatch import fnmatch
NARROW = [{'Effect': 'Allow', 'Action': ['bedrock:InvokeModel', 'bedrock:InvokeModelWithResponseStream'], 'Resource': 'arn:aws:bedrock:eu-central-1::foundation-model/anthropic.claude-*'}]
BROAD = [{'Effect': 'Allow', 'Action': ['bedrock:*'], 'Resource': '*'}]
SCP = [{'Effect': 'Deny', 'Action': 'bedrock:*', 'Resource': '*', 'NotRegions': ['eu-central-1', 'eu-west-1']}]       # org-wide guardrail
def allowed(policy, scp, action, resource, region):
    for st in scp:
        if st['Effect'] == 'Deny' and fnmatch(action, st['Action']) and region not in st.get('NotRegions', []): return False
    return any(st['Effect'] == 'Allow' and any(fnmatch(action, a) for a in st['Action']) and fnmatch(resource, st['Resource']) for st in policy)
R = lambda model, region='eu-central-1': f'arn:aws:bedrock:{region}::foundation-model/{model}'
REQ = [('invoke approved model, EU', 'bedrock:InvokeModel', R('anthropic.claude-x'), 'eu-central-1'),
       ('invoke streaming, EU', 'bedrock:InvokeModelWithResponseStream', R('anthropic.claude-x'), 'eu-central-1'),
       ('invoke a different vendor model', 'bedrock:InvokeModel', R('other.model-y'), 'eu-central-1'),
       ('invoke approved model in the US', 'bedrock:InvokeModel', R('anthropic.claude-x', 'us-east-1'), 'us-east-1'),
       ('create a guardrail', 'bedrock:CreateGuardrail', '*', 'eu-central-1'),
       ('delete a custom model', 'bedrock:DeleteCustomModel', '*', 'eu-central-1'),
       ('start a fine-tuning job', 'bedrock:CreateModelCustomizationJob', '*', 'eu-central-1'),
       ('change logging config', 'bedrock:PutModelInvocationLoggingConfiguration', '*', 'eu-central-1'),
       ('read a storage bucket', 's3:GetObject', 'arn:aws:s3:::any-bucket/key', 'eu-central-1'),
       ('invoke approved model, EU west', 'bedrock:InvokeModel', R('anthropic.claude-x', 'eu-west-1'), 'eu-west-1'),
       ('invoke a model in Asia', 'bedrock:InvokeModel', R('anthropic.claude-x', 'ap-south-1'), 'ap-south-1'),
       ('list foundation models', 'bedrock:ListFoundationModels', '*', 'eu-central-1')]
print(f'{"request":36} {"narrow role":>12} {"broad role":>11}')
n = b = 0
for name, a, res, reg in REQ:
    x, y = allowed(NARROW, SCP, a, res, reg), allowed(BROAD, SCP, a, res, reg); n += x; b += y
    print(f'{name:36} {"allowed" if x else "DENIED":>12} {"allowed" if y else "DENIED":>11}')
print(f'\nallowed: narrow role {n} of {len(REQ)} · broad role {b} of {len(REQ)}   (the Region guardrail applies to both)')
