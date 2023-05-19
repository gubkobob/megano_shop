from django.contrib import admin

from preferences.admin import PreferencesAdmin
from app_administrator.models import (LimitedEditionPreferences, PopularProductsPreferences,
                                      LimitedOffersPreferences, LimitedBannersPreferences,
                                      LimitedSlidersPreferences, PopularTagsPreferences, ViewedProductsPreferences)

admin.site.register(LimitedEditionPreferences, PreferencesAdmin)
admin.site.register(PopularProductsPreferences, PreferencesAdmin)
admin.site.register(LimitedOffersPreferences, PreferencesAdmin)
admin.site.register(LimitedBannersPreferences, PreferencesAdmin)
admin.site.register(LimitedSlidersPreferences, PreferencesAdmin)
admin.site.register(PopularTagsPreferences, PreferencesAdmin)
admin.site.register(ViewedProductsPreferences, PreferencesAdmin)
