from django.db.models import Avg
from rest_framework.decorators import APIView,api_view
from rest_framework.response import  Response
from rest_framework import status,generics
from .serializers import VendorSerializers,PurchaseOrderSerializers,PerformanceSerializers,RegisterSerilizer,LoginSerializer
from .models import vendor,purchaseOrder,Performance
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import F, ExpressionWrapper, fields


class LoginAPI(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data['username'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'status': True, 'message': 'User logged in', 'token': token.key}, status=status.HTTP_201_CREATED)

class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True, 'message': 'User created'}, status=status.HTTP_201_CREATED)

class VendorAPI(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    """List all vendor"""

    def get(self,request):
        query=vendor.objects.all()
        serializer = VendorSerializers(query,many=True)
        return Response({'message':serializer.data})

    """create a new vendor"""
    def post(self,request):
        serializer = VendorSerializers(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class VendorAPI_ID(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    """Retrieve a specific vendor's details"""
    def get(self, request,pk):
        query = vendor.objects.get(id = pk)
        serializer = VendorSerializers(query)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

    """Update a vendor's details"""
    def put(self, request,pk):
        query = vendor.objects.get(id=pk)
        serializer = VendorSerializers(query,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        query = vendor.objects.get(id=pk)
        serializer = VendorSerializers(query,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    """Delete a vendor"""
    def delete(self, request,pk):
        query = vendor.objects.get(id=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderAPI(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    """Create a purchase order"""
    def post(self,request):
        serializer = PurchaseOrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """List all purchase order with an option to fileter by vendor"""
    def get(self,request):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            query = purchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            query = purchaseOrder.objects.all()
        serializer = PurchaseOrderSerializers(query,many=True)
        if not serializer.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

class PurchaseOrderAPI_ID(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    """Retrieve details of specific purchase order"""
    def get(self,request,pk):
        try:
            query = purchaseOrder.objects.get(id=pk)
        except purchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializers(query)
        return Response(serializer.data)

    """Update a purchase order"""
    def put(self,request,pk):
        try:
            query = purchaseOrder.objects.get(id=pk)
        except purchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializers(query,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        try:
            query = purchaseOrder.objects.get(id=pk)
        except purchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializers(query, request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    """Delete a purchase order"""
    def delete(self,request,pk):
        try:
            query = purchaseOrder.objects.get(id=pk)
        except purchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        query.delete()

class VendorPerformanceView(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializers

    """Retrieve a vendor's performance metrics"""
    def get_object(self):
        pk = self.kwargs.get('pk')
        return Performance.objects.filter(vendor_id=pk).first()



class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = purchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializers

    """update acknowledgment_date and trigger the recalculation of average_response_time"""
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        acknowledgement_date = request.data.get('acknowledgement_date')
        instance.acknowledgement_date = acknowledgement_date
        instance.save()

        # Update average_response_time for the vendor
        response_times = purchaseOrder.objects.filter(
            vendor=instance.vendor,
            acknowledgement_date__isnull=False
        ).annotate(
            response_time=ExpressionWrapper(
                F('acknowledgement_date') - F('issue_date'),
                output_field=fields.DurationField()
            )
        ).aggregate(
            average_response_time=Avg('response_time')
        )['average_response_time']

        # If there are response times, update average_response_time for the vendor
        if response_times is not None:
            instance.vendor.average_response_time = response_times.total_seconds()
            instance.vendor.save()

        return Response({'acknowledgement_date': instance.acknowledgement_date})




# class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#     queryset = purchaseOrder.objects.all()
#     serializer_class = PurchaseOrderSerializers
#
#     def create(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.acknowledgment_date = request.data.get('acknowledgement_date')    #timezone.now()
#         instance.save()
#         response_times = purchaseOrder.objects.filter(vendor=instance.vendor, acknowledgement_date__isnull=False).values_list('acknowledgement_date', 'issue_date')
#         average_response_time = sum(abs((ack_date - issue_date).total_seconds()) for ack_date, issue_date in response_times) #/ len(response_times)
#         if response_times:
#             average_response_time = average_response_time / len(response_times)
#         else:
#             average_response_time = 0  # Avoid division by zero if there are no response times
#         instance.vendor.average_response_time = average_response_time
#         instance.vendor.save()
#
#         query = Performance.objects.get(vendor=instance.vendor)
#         serializers = PerformanceSerializers(query)
#         serializers.data['average_response_time'] = average_response_time
#         return Response({'acknowledgment_date': instance.acknowledgement_date})

