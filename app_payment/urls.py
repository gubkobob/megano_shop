from django.urls import path
from .views import PayView, PayView2

app_name = 'apppayment'

urlpatterns = [
    path('', PayView.as_view(), name='payment'),
    path('process/', PayView2.as_view(), name='payment2'),
    # path('good/', run_DHM, name='payment3'),
]
