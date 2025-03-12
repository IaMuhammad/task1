from django.urls import path

from apps.views import StadiumListCreateAPIView, UploadImageAPIView, StadiumRetrieveAPIView, BookStadiumCreateAPIView, \
    UserOrdersListAPIView, OrderDestroyAPIView

urlpatterns = [
    path('book-stadium', BookStadiumCreateAPIView.as_view(), name='book-stadium'),
    path('stadium', StadiumListCreateAPIView.as_view(), name='stadium'),
    path('stadium/<int:pk>', StadiumRetrieveAPIView.as_view(), name='stadium-detail'),
    path('upload-image', UploadImageAPIView.as_view(), name='upload-image'),
    path('user-orders', UserOrdersListAPIView.as_view(), name='user-orders'),
    path('order-delete/<int:pk>', OrderDestroyAPIView.as_view(), name='order-delete'),
]
