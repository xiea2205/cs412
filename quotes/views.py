from django.shortcuts import render
import random

# Lists of quotes and images from Albert Einstein
quotes = [
    "Imagination is more important than knowledge.",
    "Try not to become a person of success, but rather try to become a person of value.",
    "Life is like riding a bicycle. To keep your balance, you must keep moving.",
]

images = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Albert_Einstein_Head.jpg/256px-Albert_Einstein_Head.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Einstein_1921_portrait2.jpg/256px-Einstein_1921_portrait2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg/256px-Einstein_1921_by_F_Schmutzer_-_restoration.jpg",
]

def quote(request):
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    context = {
        'quote': random_quote,
        'image': random_image,
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    context = {
        'quotes': quotes,
        'images': images,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    return render(request, 'quotes/about.html')
