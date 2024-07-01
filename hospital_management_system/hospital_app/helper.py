from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Patient
from rest_framework import status
from rest_framework.response import Response


class ContactNumberFilterMixin:
    patient_separator = ","

    def filter_by_contact_number(self, queryset, contact_number_field):
        contactnumber = self.request.query_params.get("contactnumber", None)
        if contactnumber:
            contact_numbers = contactnumber.split(self.patient_separator)
            filter_kwargs = {f"{contact_number_field}__in": contact_numbers}
            queryset = queryset.filter(**filter_kwargs)
        return queryset
    
class Patient_List_from_patient(ContactNumberFilterMixin):
    def get_queryset(self):
        return self.filter_by_contact_number(super().get_queryset(), "contact_number")

class Patient_List_from_patentvisit(ContactNumberFilterMixin):
    def get_queryset(self):
        return self.filter_by_contact_number(super().get_queryset(), "patient__contact_number")


class LoginAPIView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        
        return Response({"token": token.key, "user": serializer.data})

class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CRUDHelper:
    model = None
    serializer_class = None

    @classmethod
    def get_all(cls):
        instances = cls.model.objects.all()
        serializer = cls.serializer_class(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def get_instance(cls, pk):
        try:
            instance = cls.model.objects.get(pk=pk)
            serializer = cls.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except cls.model.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def create_instance(cls, data):
        serializer = cls.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def update_instance(cls, contact_number, data, partial=False):
        try:
            patient = Patient.objects.get(contact_number=contact_number)
            instance = cls.model.objects.get(patient=patient)
            serializer = cls.serializer_class(instance, data=data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        except cls.model.DoesNotExist:
            return Response({'error': 'Patient visit not found'}, status=status.HTTP_404_NOT_FOUND)


    @classmethod
    def get_patient(cls):
        instance = cls.model.objects.all()
        serializer = cls.serializer_class(instance,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)