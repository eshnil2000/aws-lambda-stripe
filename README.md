# aws-lambda-stripe
* Based on https://www.proud2becloud.com/how-to-create-a-serverless-payment-system-using-stripe-and-aws-lambda/
* In IAM, Create new policy to allow role stripe-role-xxx to access secrets manager

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
