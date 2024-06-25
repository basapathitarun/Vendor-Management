from django.urls import path
from .views import VendorAPI,VendorAPI_ID,PurchaseOrderAPI,PurchaseOrderAPI_ID\
    ,VendorPerformanceView,AcknowledgePurchaseOrderView,RegisterAPI,LoginAPI

urlpatterns = [
    path('login/',LoginAPI.as_view()),
    path('register/',RegisterAPI.as_view()),
    path('vendor/',VendorAPI.as_view(),name='vendor'),
    path('vendor/<int:pk>/',VendorAPI_ID.as_view()),
    path('purchase_orders/',PurchaseOrderAPI.as_view()),
    path('purchase_orders/<int:pk>/',PurchaseOrderAPI_ID.as_view()),
    path('vendor/<int:pk>/performance', VendorPerformanceView.as_view()),
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view()),
]