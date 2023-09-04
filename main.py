from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hu():
  return {"msg": "Hello world!"}

@app.get("/meal")
def calculate_meal_fee(beef_price: int, meal_price: int) -> int:
  total_price: int = beef_price + meal_price
  return total_price