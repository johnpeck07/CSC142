import random

class Review:
    def __init__(self, rating, text):
        self.rating = rating      # number from 0–5
        self.text = text          # review text

    def __str__(self):
        return f"Rating: {self.rating}/5 - {self.text}"


class Movie:
    def __init__(self, title):
        self.title = title
        self.reviews = []         # list of Review objects

    def add_review(self, review):
        self.reviews.append(review)

    def average_rating(self):
        if len(self.reviews) == 0:
            return 0
        total = 0
        for review in self.reviews:
            total += review.rating
        return total / len(self.reviews)

    def display_reviews(self):
        for review in self.reviews:
            print(review)

    def best_review(self):
        if len(self.reviews) == 0:
            return None
        highest = max(review.rating for review in self.reviews)
        best_reviews = [r for r in self.reviews if r.rating == highest]
        return random.choice(best_reviews)

    def worst_review(self):
        if len(self.reviews) == 0:
            return None
        lowest = min(review.rating for review in self.reviews)
        worst_reviews = [r for r in self.reviews if r.rating == lowest]
        return random.choice(worst_reviews)


# ---------------- Driver Code ----------------

movie = Movie("The Matrix")

review1 = Review(5, "Amazing movie with great action.")
review2 = Review(4, "Very good, but a little confusing.")
review3 = Review(2, "Not my favorite.")

movie.add_review(review1)
movie.add_review(review2)
movie.add_review(review3)

print("Movie:", movie.title)
print("Average Rating:", movie.average_rating())
print("\nAll Reviews:")
movie.display_reviews()

print("\nBest Review:")
print(movie.best_review())

print("\nWorst Review:")
print(movie.worst_review())