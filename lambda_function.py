import stripe
import boto3
import json

client = boto3.client('secretsmanager')
keys = json.loads(client.get_secret_value(
  SecretId = 'arn:aws:secretsmanager:us-east-1:account-number:secret:secret-name',
)['SecretString'])
public_key = keys['stripe-public']
secret_key = keys['stripe-secret']
stripe.api_key = secret_key

def lambda_handler(event, context):
  signup(event, context)

def signup(event, context):
  card_data = event.get('cardData')
  email = event.get('email')
  attributes = event.get('attributes')
  response=create_stripe_customer(email, attributes, card_data)
  print(response)
  return event

def create_stripe_customer(email, user_data, payment_info):
  response = stripe.Customer.create(email = email, metadata = user_data)
  customer_id=response['id']
  
  #customer_id='ID for test'
  payment_method_id = create_payment_method(payment_info)
  print("payment method ID is..."+payment_method_id )
  response=stripe.PaymentMethod.attach(
    payment_method_id,
    customer = customer_id
  )
  print("Attaching payment_info to customer")
  print(response)
  stripe.Customer.modify(customer_id,invoice_settings={"default_payment_method":payment_method_id})
  
  
  response=create_stripe_plan(customer_id)
  print(response)
  return {
    "customer_id": customer_id,
    "plan": response
  }

def create_payment_method(payment_info):
  response= stripe.PaymentMethod.create(
    type = "card",
    card = {
      "number": payment_info.get('cardNumber'),
      "exp_month": payment_info.get('expirationMonth'),
      "exp_year": payment_info.get('expirationYear'),
      "cvc": payment_info.get('ccv'),
    })
  print(response)
  return response['id']

def create_stripe_plan(customer_id):
   
  response= stripe.Subscription.create(
    customer = customer_id,
    items = [{
      "plan": "price_ID"
    }]
  )
  return response['id']
