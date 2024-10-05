from ..models import(
    EventType,
    Event,
    Role,
)
from django.db.models import Case, When, IntegerField
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import SchoolHeader, IsDirectiveOrOnlyRead
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime
from ..serializers.event_serializer import EventSerializer, EventTypeSerializer, CreateEventSerializer
from ..serializers.roles_serializer import RoleSerializer



class EventListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        school = self.request.school
        user = self.request.user
        roles = self.request.query_params.getlist('rolesIds', None)
        rol = self.request.query_params.get('role', None)
        queryset = Event.objects.filter(school=school)

        if user.is_preceptor(school) and rol == 'Preceptor':
            queryset = queryset.filter(roles__name__in=["Preceptor", "Profesor"])
        elif user.is_teacher(school) and rol == 'Profesor':
            queryset = queryset.filter(roles__name="Profesor")
        if roles:
            queryset = queryset.filter(roles__in=roles)

        current_time = datetime.now()
        queryset = queryset.annotate(
            event_status=Case(
                When(startDate__lte=current_time, endDate__gte=current_time, then=1),  # En Curso
                When(startDate__gt=current_time, then=2),  # Pendiente
                When(endDate__lt=current_time, then=3),  # Finalizado
                output_field=IntegerField(),
            )
        ).order_by('event_status', 'startDate')

        name = self.request.query_params.get('name', None)
        event_type = self.request.query_params.get('eventType', None)
        max_date = self.request.query_params.get('maxDate', None)
        roles = self.request.query_params.getlist('rolesIds', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if event_type:
            queryset = queryset.filter(eventType_id=event_type)
        if max_date:
            try:
                max_date = max_date.replace('%2F', '/')
                max_date_parsed = datetime.strptime(max_date, '%d/%m/%Y')
                queryset = queryset.filter(startDate__lte=max_date_parsed)
            except ValueError:
                raise ValidationError("La fecha proporcionada no tiene el formato correcto. Use 'dd/mm/yyyy'.")
        if roles:
            try:
                for role in roles:
                    role_id = int(role)
                    if not Role.objects.filter(pk=role_id).exists():
                        raise ValidationError({'error': '"roles_ids": no valido.'})
            except ValueError:
                    raise ValidationError("Los roles proporcionados no existen.")
                
        return queryset.distinct()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({'detail': 'Not found event.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            data = self.request.data
            data['school'] = self.request.school.pk
            kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventSerializer
        return CreateEventSerializer
    
    def perform_create(self, serializer):
        serializer.save(school=self.request.school)
      

class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventSerializer
        return CreateEventSerializer
        
    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'PUT':
            data = self.request.data
            data['school'] = self.request.school.pk
            kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(school=self.request.school)

class AffiliatedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader]

    def post(self, request, *args, **kwargs):
        """
        Se le indica el evento y el usuario que sera adherido.
        """
        return self.manage_user(request, is_add=True)
    
    def delete(self, request, *args, **kwargs):
        """
        Se le indica el evento y el usuario que sera desadherido.
        """
        return self.manage_user(request, is_add=False)

    def manage_user(self, request, is_add):
        event_id = request.data.get('event_id')
        user = request.user
        school = request.school
        if not event_id:
            return Response({'detail': '"event_id" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            event: Event = Event.objects.get(pk=event_id)
        except (Event.DoesNotExist):
            return Response({'detail': 'Event do not exist'}, status=status.HTTP_404_NOT_FOUND)

        if event.school != school:
            return Response({'detail': 'Event not recognized at school'})
        
        event_roles = set(event.roles.values_list('name', flat=True))
        user_roles = set()

        if user.is_directive(school):
            user_roles.add('Directivo')
        if user.is_teacher(school):
            user_roles.add('Profesor')
        if user.is_preceptor(school):
            user_roles.add('Preceptor')

        if not user_roles & event_roles: 
            return Response({'detail': 'User does not have the required role for this event'}, status=status.HTTP_403_FORBIDDEN)

        if is_add:
            if user in event.affiliated_teachers.all():
                return Response({'detail': 'User is already a affiliated.'})
            event.affiliated_teachers.add(user)
            status_code = status.HTTP_201_CREATED
        else:
            if user not in event.affiliated_teachers.all():
                return Response({'error': 'The user is not associated with event.'}, status=status.HTTP_400_BAD_REQUEST)
            event.affiliated_teachers.remove(user)
            status_code = status.HTTP_200_OK
        
        event.save()
        return Response(status=status_code)


class EventTypeViewSet(generics.ListAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class RoleView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserRolesViewSet(APIView):
    permission_classes = [IsAuthenticated, SchoolHeader]

    def get(self, request):
        user = request.user
        school = request.school

        roles = []
        if user.is_directive(school):
            roles.append('Directivo')
        if user.is_teacher(school):
            roles.append('Profesor')
        if user.is_preceptor(school):
            roles.append('Preceptor')

        return Response({
            'roles': roles
        })
    