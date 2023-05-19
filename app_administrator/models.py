from preferences.models import Preferences
from app_catalog.models import *
from app_banners.models import *


class LimitedEditionPreferences(Preferences):
    """ Ограниченный тираж. """
    limited_products = models.ForeignKey(Product, on_delete=models.CASCADE)
    pass


class PopularProductsPreferences(Preferences):
    """ Популярные товары. """
    popular_products = models.ForeignKey(Product, on_delete=models.CASCADE)
    pass


class LimitedOffersPreferences(Preferences):
    """ Ограниченные предложения. """
    limited_offers = models.ForeignKey(Product, on_delete=models.CASCADE)
    pass


class LimitedBannersPreferences(Preferences):
    """ Количество отображения баннеров. """
    pass


class LimitedSlidersPreferences(Preferences):
    """ Изменение количества отображения рекламы. """
    pass


class PopularTagsPreferences(Preferences):
    """ Популярные теги. """
    pass


class ViewedProductsPreferences(Preferences):
    """  Изменение вывода просмотренных товаров. """
    viewed_products = models.ForeignKey(Product, on_delete=models.CASCADE)
    pass
