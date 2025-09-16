from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time
from datetime import datetime, timedelta

def main(request):
    """View for the main restaurant page"""
    return render(request, 'restaurant/main.html')

def order(request):
    """View for the order page with daily special"""
    daily_specials = [
        {"name": "Grilled Salmon Special", "description": "Fresh Atlantic salmon with lemon herb butter", "price": 24.99},
        {"name": "Pasta Primavera Special", "description": "Fresh vegetables with penne pasta in garlic cream sauce", "price": 18.99},
        {"name": "BBQ Ribs Special", "description": "Fall-off-the-bone ribs with house BBQ sauce", "price": 22.99},
        {"name": "Vegetarian Curry Special", "description": "Coconut curry with seasonal vegetables and basmati rice", "price": 16.99},
        {"name": "Steak Frites Special", "description": "Grilled sirloin with crispy fries and garlic aioli", "price": 26.99}
    ]
    
    daily_special = random.choice(daily_specials)
    
    context = {
        'daily_special': daily_special
    }
    
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    """View to process order form and display confirmation"""
    if request.method == 'POST':
        # Menu items with prices
        menu_items = {
            'burger': {'name': 'Classic Burger', 'price': 12.99},
            'pizza': {'name': 'Margherita Pizza', 'price': 16.99},
            'salad': {'name': 'Caesar Salad', 'price': 10.99},
            'pasta': {'name': 'Spaghetti Carbonara', 'price': 14.99}
        }
        
        # Get ordered items
        ordered_items = []
        total_price = 0.0
        
        # Check for regular menu items
        for item_key, item_info in menu_items.items():
            if request.POST.get(item_key):
                ordered_items.append(item_info)
                total_price += item_info['price']
        
        # Check for daily special
        if request.POST.get('daily_special'):
            special_name = request.POST.get('special_name', 'Daily Special')
            special_price = float(request.POST.get('special_price', 0))
            ordered_items.append({'name': special_name, 'price': special_price})
            total_price += special_price
        
        # Get customer information
        customer_name = request.POST.get('customer_name', '')
        customer_phone = request.POST.get('customer_phone', '')
        customer_email = request.POST.get('customer_email', '')
        special_instructions = request.POST.get('special_instructions', '')
        
        # Calculate ready time (30-60 minutes from now)
        minutes_to_add = random.randint(30, 60)
        ready_time = datetime.now() + timedelta(minutes=minutes_to_add)
        
        context = {
            'ordered_items': ordered_items,
            'total_price': total_price,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'ready_time': ready_time
        }
        
        return render(request, 'restaurant/confirmation.html', context)
    
    # If not POST, redirect to order page
    from django.shortcuts import redirect
    return redirect('order')
