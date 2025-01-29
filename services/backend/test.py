import requests
from faker import Faker

BASE_URL = "http://backend:8000/api/v1"

create_category_url = f"{BASE_URL}/category/create"
create_review_url = f"{BASE_URL}/reviews/create"
get_reviews_trends_url = f"{BASE_URL}/reviews/trends"
get_reviews_url = f"{BASE_URL}/reviews"

fake = Faker()

# Function to create a category
def create_category(category_data):
    print(f"Creating category: {category_data['name']}")
    response = requests.post(create_category_url, json=category_data)
    if response.status_code == 200:
        category = response.json()
        print(f"Category '{category_data['name']}' created successfully. ID: {category['id']}")
        return category["id"]
    else:
        print(f"Failed to create category '{category_data['name']}': {response.text}")
        return None

# Function to create a review (parent or edit)
def create_review(review_data):
    if review_data["review_id"]:
        print(f"Creating edit for Review ID {review_data['review_id']}")
    else:
        print(f"Creating parent review for Category ID {review_data['category_id']}")
    response = requests.post(create_review_url, json=review_data)
    if response.status_code == 200:
        review = response.json()
        review_id = review["id"]
        print(f"Review created successfully. ID: {review_id}")
        return review_id
    else:
        print(f"Failed to create review for Category ID {review_data['category_id']}: {response.text}")
        return None

# Function to test the /trends endpoint (Get top categories based on average stars)
def test_trends():
    print("Fetching top 5 categories based on average stars...")
    response = requests.get(get_reviews_trends_url)
    if response.status_code == 200:
        trends = response.json()
        print("Top 5 categories based on average stars:")
        for trend in trends:
            print(f"Category: {trend['name']}, Avg Stars: {trend['average_stars']}")
        return trends
    else:
        print(f"Failed to fetch trends: {response.text}")
        return None

# Function to test the /reviews endpoint (Get reviews by category)
def test_get_reviews(category_id):
    print(f"Fetching reviews for Category ID {category_id}...")
    response = requests.get(get_reviews_url, params={"category_id": category_id})
    if response.status_code == 200:
        reviews = response.json()
        print(f"Reviews for Category ID {category_id}:")
        for review in reviews:
            print(f"Review ID: {review['id']}, Stars: {review['stars']}, Text: {review['text']}")
        return reviews
    else:
        print(f"Failed to fetch reviews for Category ID {category_id}: {response.text}")
        return None

# Function to create categories and reviews for each category
def create_categories_and_reviews():
    print("Starting category and review creation...")

    category_ids = []
    for i in range(5):
        category_data = {"name": fake.word(), "description": fake.text()}
        category_id = create_category(category_data)
        if category_id:
            category_ids.append(category_id)

    # Create 5 reviews and 3 edits for each category
    for category_id in category_ids:
        print(f"\nCreating reviews for Category ID {category_id}...")

        # Step 1: Create 5 parent reviews, one for each category
        for i in range(5):
            parent_review_data = {
                "stars": fake.random_int(1, 10),
                "text": fake.sentence(),
                "category_id": category_id,
                "review_id": None
            }
            parent_review_id = create_review(parent_review_data)

            if parent_review_id:
                # Step 2: Create 3 edits for each parent review
                print(f"Creating edits for Parent Review ID {parent_review_id}...")
                for j in range(3):
                    edit_review_data = {
                        "stars": fake.random_int(1, 10),
                        "text": fake.sentence(),
                        "category_id": category_id,
                        "review_id": parent_review_id
                    }
                    create_review(edit_review_data)

    print("Category and review creation completed.")

    # Run tests (fetch trends and reviews)
    print("\nRunning tests...\n")
    trends = test_trends()
    if trends:
        print(f"Total Top Categories: {len(trends)}")

    # Fetch reviews for each category (test endpoint)
    for category_id in category_ids:
        test_get_reviews(category_id)

# Execute the function to create categories and reviews
create_categories_and_reviews()
