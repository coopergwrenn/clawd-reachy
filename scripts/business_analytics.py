#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Business analytics - pull key metrics for all businesses
"""
import json
import stripe
from datetime import datetime, timedelta

def load_stripe_key():
    with open('/home/wrenn/clawd/stripe-credentials.json', 'r') as f:
        data = json.load(f)
    return data['api_key']

def get_business_metrics():
    """Get comprehensive business metrics"""
    stripe.api_key = load_stripe_key()
    
    # Last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    week_timestamp = int(week_ago.timestamp())
    
    # Last 30 days
    month_ago = datetime.now() - timedelta(days=30)
    month_timestamp = int(month_ago.timestamp())
    
    # Get charges
    week_charges = stripe.Charge.list(created={'gte': week_timestamp}, limit=100)
    month_charges = stripe.Charge.list(created={'gte': month_timestamp}, limit=100)
    
    # Get customers
    week_customers = stripe.Customer.list(created={'gte': week_timestamp}, limit=100)
    month_customers = stripe.Customer.list(created={'gte': month_timestamp}, limit=100)
    
    # Calculate metrics
    week_revenue = sum(c.amount for c in week_charges.data if c.paid) / 100
    month_revenue = sum(c.amount for c in month_charges.data if c.paid) / 100
    
    week_customer_count = len(week_customers.data)
    month_customer_count = len(month_customers.data)
    
    # Get balance
    balance = stripe.Balance.retrieve()
    available_balance = sum(b['amount'] for b in balance.available) / 100
    
    # Calculate MRR estimate (last 30 days annualized / 12)
    mrr = (month_revenue / 30 * 365) / 12
    
    return {
        'last_7_days': {
            'revenue': week_revenue,
            'customers': week_customer_count,
            'charges': len([c for c in week_charges.data if c.paid])
        },
        'last_30_days': {
            'revenue': month_revenue,
            'customers': month_customer_count,
            'charges': len([c for c in month_charges.data if c.paid])
        },
        'mrr_estimate': mrr,
        'available_balance': available_balance,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    metrics = get_business_metrics()
    print(json.dumps(metrics, indent=2))
