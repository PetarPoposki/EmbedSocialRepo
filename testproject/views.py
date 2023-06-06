import json
from django.shortcuts import render

# Load reviews data from the reviews.json file
with open('../reviews.json') as f:
    reviews_data = json.load(f)

def filter_reviews(request):
    reviews = reviews_data  # Initial reviews data

    # Get filter options from request.GET
    text_filter = request.GET.get('text_filter')
    rating_filter = request.GET.get('rating_filter')
    date_filter = request.GET.get('date_filter')
    minimum_rating = request.GET.get('minimum_rating')

    # Apply filters
    if text_filter == 'Yes':
        reviews = [review for review in reviews if review['reviewText']]
    if minimum_rating:
        minimum_rating = int(minimum_rating)
        reviews = [review for review in reviews if review['rating'] >= minimum_rating]

    # Sort the reviews
    if rating_filter == 'Highest First':
        reviews = sorted(reviews, key=lambda x: (x['reviewText'], -x['rating'], x['reviewCreatedOnDate']))
    elif rating_filter == 'Lowest First':
        reviews = sorted(reviews, key=lambda x: (x['reviewText'], x['rating'], x['reviewCreatedOnDate']))
    else:
        reviews = sorted(reviews, key=lambda x: (x['reviewText'], x['reviewCreatedOnDate']))

    if date_filter == 'Newest First':
        reviews.reverse()

    context = {
        'reviews': reviews
    }

    return render(request, 'reviews.html', context)
