from haystack import indexes
from .models import Restaurant, Dish

class RestaurantIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True)
	
	def get_model(self):
		return Restaurant
		