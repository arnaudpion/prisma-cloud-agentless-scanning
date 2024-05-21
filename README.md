# prisma-cloud-agentless-scanning
Scripts to update agentless scanning configuration in bulk in Prisma Cloud

## agentless-scanning-aws-bulk-update.py
This python script allows you to bulk update the agentless scanning configuration of AWS accounts.

### Usage
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 agentless-scanning-aws-bulk-update.py
```

### Requirements
- Onboard your AWS accounts in Prisma Cloud. Make sure they have the _Agentless Workload Scanning_ capability selected during onboarding
- Create an Access Key on Prisma Cloud, you can refer to the [online documentation](https://docs.prismacloud.io/en/enterprise-edition/content-collections/administration/create-access-keys)
- Create Environment Variables on your system :
  - **COMPUTE_API_ENDPOINT** : url of your [Prisma Cloud Compute Console](https://pan.dev/prisma-cloud/api/cwpp/access-api-saas/#:~:text=Retrieve%20your%20Compute%20Console's%20address,your%20Prisma%20Cloud%20user%20credentials)
  - **PRISMA_USERNAME** : your Prisma Cloud Access Key
  - **PRISMA_PASSWORD** : your Prisma Cloud Secret Key
- Modify the values of the following variables in the script :
  - **AWS_REGIONS** : the list of AWS regions you want to scan
  - **HUB_ACCOUNT** : the name or AWS ID of the AWS account you want to use as hub account
    - if your AWS accounts are onboarded as standalone accounts (no AWS Organization), put the name of the account in Prisma Cloud, example : "aws-hub"
    - if your AWS accounts are onboarded as part of an AWS Organization, put the ID of the account, example : "123412341234"

### Credits
Stephen Gordon, who worked on the initial script used as baseline for this one