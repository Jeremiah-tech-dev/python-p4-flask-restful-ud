#!/usr/bin/env python3
import sqlite3
import random
from datetime import datetime

conn = sqlite3.connect('newsletters.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM newsletters')

titles = [
    "Tech News Weekly", "Product Updates", "Company Newsletter", 
    "Industry Insights", "Monthly Digest", "Breaking News",
    "Feature Spotlight", "Customer Stories", "Team Updates",
    "Market Analysis"
]

bodies = [
    "This week we have exciting updates to share with our community.",
    "Check out the latest features and improvements we've made.",
    "Here's what's happening in the industry this month.",
    "We're thrilled to announce some major developments.",
    "Stay informed with our latest insights and analysis.",
    "Discover how our customers are achieving success.",
    "Learn about the newest additions to our platform.",
    "Get the inside scoop on what our team has been working on.",
    "Explore the trends shaping our industry today.",
    "Find out what's new and what's next for us."
]

for i in range(50):
    title = random.choice(titles) + f" #{i+1}"
    body = random.choice(bodies) + " " + random.choice(bodies)
    cursor.execute(
        'INSERT INTO newsletters (title, body, published_at) VALUES (?, ?, ?)',
        (title, body, datetime.now())
    )

conn.commit()
conn.close()
print("Seeded 50 newsletters!")
