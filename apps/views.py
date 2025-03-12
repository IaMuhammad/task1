from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.filterset import StadiumListFilter
from apps.models import Stadium, Order
from apps.permissions import IsOwnerPermission, IsAdminOrSupperUser
from apps.serializers import StadiumPostSerializer, UploadImageSerializer, StadiumDetailSerializer, \
    StadiumListSerializer, BookStadiumSerializer, OrderModelSerializer


# Create your views here.
class BookStadiumCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = BookStadiumSerializer
    permission_classes = (IsAuthenticated,)


class StadiumListCreateAPIView(ListCreateAPIView):
    queryset = Stadium.objects.all()
    parser_classes = (MultiPartParser,)
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StadiumListFilter

    # def get_permissions(self):
    #     return self.permission_class_dict.get(self.request.method, (IsAuthenticated,))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class_dict = {
            'POST': StadiumPostSerializer,
            'GET': StadiumListSerializer
        }
        self.permission_class_dict = {
            'POST': (IsAdminOrSupperUser,),
            'GET': (IsAuthenticated,)
        }

    def get_serializer_class(self):
        return self.serializer_class_dict[self.request.method]


class UserOrdersListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user',)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDestroyAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = (IsOwnerPermission,)


class StadiumRetrieveAPIView(RetrieveAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumDetailSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (AllowAny,)


class UploadImageAPIView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(request=UploadImageSerializer, responses=[])
    def post(self, request, *args, **kwargs):
        serializer = UploadImageSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=201)
