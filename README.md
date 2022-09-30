# aws-lambda-stripe
* Based on https://www.proud2becloud.com/how-to-create-a-serverless-payment-system-using-stripe-and-aws-lambda/
*** Add layers to lambda with https://dev.to/mmascioni/using-external-python-packages-with-aws-lambda-layers-526o
- Create virtualenv on laptop
```
virtualenv lambda-layers-stripe
source lambda-layers-stripe/bin/activate
mkdir python
pip install -r requirements.txt --target python
zip -r layer python/
```
- Contents of requirements.txt
```
pip
stripe
boto3
```

* In IAM, Create new policy to allow role stripe-role-xxx to access secrets manager
***
```xxxf656a8d-146d-422f-b79f-efcdcf05089a	Customer managed	

stripe-lambda-secrets-manager-access	Customer inline	
```
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetResourcePolicy",
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret",
                "secretsmanager:ListSecretVersionIds"
            ],
            "Resource": "arn:aws:secretsmanager:us-east-1:account_id:secret:stripe-name"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetRandomPassword",
                "secretsmanager:ListSecrets"
            ],
            "Resource": "*"
        }
    ]
}
```

*** test Lambda 
```
{
  "cardData": {
    "cardNumber": "3782 822463 10005",
    "expirationMonth": "12",
    "expirationYear": "2024",
    "ccv": "123"
  },
  "email": "test@test.com",
  "attributes": {}
}

```
***Create new product , add price, use PRICE_ID NOT Product_ID
