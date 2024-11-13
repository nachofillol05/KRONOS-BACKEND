from ..models import(
    Subject,
    Year, 
    Module,
    Course,
    CourseSubjects
)
from django.http import HttpResponse
from django.db.models import  Case, When
from rest_framework.permissions import IsAuthenticated
from ..permissions import SchoolHeader, IsDirectiveOrOnlyRead
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from datetime import datetime
import pandas as pd
from ..serializers.school_serializer import ReadSchoolSerializer, ModuleSerializer
from ..serializers.Subject_serializer import SubjectWithCoursesSerializer, SubjectSerializer
from ..serializers.course_serializer import CourseSerializer, CreateCourseSerializer
from ..serializers.cousesubject_serializer import CourseSubjectSerializer, CourseSubjectSerializerDetail
from ..serializers.year_serializer import YearSerializer
from ..serializers.module_serializer import ModuleSerializer



class SchoolView(generics.RetrieveUpdateAPIView):
    '''
    VISTA PARA OBTENER LAS ESCUELAS DEL DIRECTIVO
    '''
    serializer_class = ReadSchoolSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get_object(self):
        return self.request.school

class SubjectListCreate(generics.ListCreateAPIView):
    '''
    LISTAR Y CREAR MATERIAS
    '''
    queryset = Subject.objects.all()
    serializer_class = SubjectWithCoursesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        teacher = request.query_params.get('teacher')
        name = request.query_params.get('name')
        school = self.request.school
        
        queryset = Subject.objects.filter(school=school).exclude(name="freeSubject")

        
        if start_time and end_time:
            queryset = queryset.filter(
                coursesubjects__teachersubjectschool__schedules__module__startTime__gte=start_time,
                coursesubjects__teachersubjectschool__schedules__module__endTime__lte=end_time
            )
        
        if teacher:
            queryset = queryset.filter(
                coursesubjects__teachersubjectschool__teacher__id=teacher
            )
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        queryset = queryset.distinct()
        
        if 'export' in request.GET and request.GET['export'] == 'excel':
            return self.export_to_excel(queryset)

        serializer = SubjectWithCoursesSerializer(queryset, many=True, context={'teacher': teacher})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        create_serializer = SubjectSerializer(data=self.request.data, context={"request": request})
        create_serializer.is_valid(raise_exception=True)
        create_serializer.save(school=self.request.school)
        return Response(
            {'Saved': 'La materia ha sido creada', 'data': create_serializer.data},
            status=status.HTTP_201_CREATED
        )

    def export_to_excel(self, queryset):
        # Convertir el queryset a un DataFrame de pandas
        data = list(queryset.values('id','name', 'abbreviation', 'color', 'coursesubjects__course__name'))

        df = pd.DataFrame(data)

        df = df.rename(columns={
        'id': 'ID',
        'name': 'Nombre',
        'abbreviation': 'Abreviatura',
        'color': 'Color',
        'coursesubjects__course__name': 'Nombre del Curso'
        })

        # Crear un archivo Excel en la memoria utilizando un buffer
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Materias.xlsx'
        
        # Escribir el DataFrame en un archivo Excel usando pandas
        df.to_excel(response, index=False, sheet_name='Materias')
        
        return response
    
    # def post(self, request):
    #     serializer = SubjectSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response(
    #         {'Saved': 'La materia ha sido creada', 'data': serializer.data},status=status.HTTP_201_CREATED)


class SubjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectWithCoursesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'Deleted': 'La materia ha sido eliminada'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({'Updated': 'La materia ha sido actualizada', 'data': response.data}, status=status.HTTP_200_OK)


class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get_queryset(self):
        school = self.request.school
        return Course.objects.filter(year__school = school).order_by('year__number', 'name')
    
    def post(self, request):
        year_number = request.data.get('year')

        try:
            Year.objects.get(pk=year_number)
        except Year.DoesNotExist:
            return Response({'Error': 'El año especificado no existe.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateCourseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            {'Saved': 'El curso ha sido creado', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )


class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CreateCourseSerializer
        return super().get_serializer_class()

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'Deleted': 'El curso ha sido eliminado'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({'Updated': 'El curso ha sido actualizado', 'data': response.data}, status=status.HTTP_200_OK)

class CourseSubjectListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = CourseSubjects.objects.all()
    serializer_class = CourseSubjectSerializer
    
    def get_queryset(self):
        queryset = CourseSubjects.objects.filter(course__year__school = self.request.school)
        if not queryset.exists():
            return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return queryset
    
    def post (self, request, *args, **kwargs):
        serializer = CourseSubjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {'Saved': 'La materia se ha asignado a un curso', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )


class CourseSubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    serializer_class = CourseSubjectSerializerDetail

    def get_queryset(self):
        queryset = CourseSubjects.objects.filter(course__year__school = self.request.school)
        return queryset

class YearListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def get_queryset(self):
        queryset = Year.objects.filter(school=self.request.school).order_by('number')
        if not queryset.exists():
            return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return queryset
    
    def perform_create(self, serializer):
        school = self.request.school
        serializer.save(school=school)

class YearRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'Deleted': 'El año ha sido eliminado'}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({'Updated': 'El año ha sido actualizado', 'data': response.data}, status=status.HTTP_200_OK)
    

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        school = validated_data.get('school')
        if school != self.request.school:
            raise ValidationError({'school': ['You can only modify the school you belong to']})
        serializer.save()

    def get_queryset(self):
        current_time = datetime.now()
        queryset = Module.objects.filter(school=self.request.school)
        queryset = queryset.annotate(
            event_status=Case(
            When(day='lunes', then=1), 
            When(day='martes', then=2),
            When(day='miércoles', then=3),
            When(day='jueves', then=4),
            When(day='viernes', then=5),
            )
        ).order_by('event_status','startTime','moduleNumber')
        day = self.request.query_params.get('day')
        if day:
            queryset = queryset.filter(day=day)
        
        return queryset
        
