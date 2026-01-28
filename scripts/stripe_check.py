#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check Stripe for today's revenue and customers
"""
import json
import stripe
from datetime import datetime, timedelta

def load_stripe_key():
    with open('/home/wrenn/clawd/stripe-credentials.json', 'r') as f:
        data = json.load(f)
    return data['api_key']

def get_stripe_data(days=1):
    try:
        stripe.api_key = load_stripe_key()
        
        # Calculate timestamp for 'days' ago
        start_time = datetime.now() - timedelta(days=days)
        start_timestamp = int(start_time.timestamp())
        
        # Get charges from the period
        charges = stripe.Charge.list(
            created={'gte': start_timestamp},
            limit=100
        )
        
        # Get customers from the period
        customers = stripe.Customer.list(
            created={'gte': start_timestamp},
            limit=100
        )
        
        # Calculate totals
        total_revenue = sum(charge.amount for charge in charges.data if charge.paid) / 100
        total_charges = len([c for c in charges.data if c.paid])
        new_customers = len(customers.data)
        
        # Get balance
        balance = stripe.Balance.retrieve()
        available_balance = sum(b['amount'] for b in balance.available) / 100
        
        return {
            'period_days': days,
            'total_revenue': total_revenue,
            'total_charges': total_charges,
            'new_customers': new_customers,
            'available_balance': available_balance,
            'recent_charges': [
                {
                    'amount': c.amount / 100,
                    'description': c.description,
                    'customer_email': c.billing_details.email if c.billing_details else None,
                    'created': datetime.fromtimestamp(c.created).strftime('%Y-%m-%d %H:%M')
                }
                for c in charges.data[:10]
            ]
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    import sys
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = get_stripe_data(days)
    print(json.dumps(data, indent=2))
