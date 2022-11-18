from django.core.paginator import Paginator

def paginator(recipes, NUMBER_OF_RECIPES, page_number):
    paginator_obj = Paginator(recipes, NUMBER_OF_RECIPES)
    return paginator_obj.get_page(page_number)
