import random
from locust import HttpUser, task, between


class BooksApiUser(HttpUser):
  wait_time = between(1, 2)

  @task(3)
  def get_books(self):
    self.client.get('/books')

  @task(1)
  def search_by_year(self):
    year = random.randint(2000, 2025)
    
    if random.random() < 0.01:
      self.client.get(f'/books/search?year={year}', status_code=500)
    else:
      self.client.get(f'/books/search?year={year}')