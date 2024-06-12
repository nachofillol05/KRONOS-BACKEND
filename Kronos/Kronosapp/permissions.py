from rest_framework import permissions
from rest_framework import exceptions
from .models import School, CustomUser


class SchoolHeader(permissions.BasePermission):
    MESSAGE_NOT_SCHOOL_ID = "Not provide school id in request headers."
    MESSAGE_SCHOOL_NOT_RECOGNIZED = "Unrecognized school."
    
    def has_permission(self, request, view):
        school_id = request.META.get('HTTP_SCHOOL_ID')
        if not school_id:
            raise exceptions.PermissionDenied(self.MESSAGE_NOT_SCHOOL_ID)
        
        try:
            school = School.objects.get(pk=school_id)
        except School.DoesNotExist:
            raise exceptions.PermissionDenied(self.MESSAGE_SCHOOL_NOT_RECOGNIZED)
        
        request.school = school
        return True


class IsDirectiveOrOnlyRead(permissions.BasePermission):
    MESSAGE_NOT_SCHOOL_DIRECTOR = "User is not a school director."

    def has_permission(self, request, view):
        user: CustomUser = request.user
        school = request.school

        is_safe_method = request.method in permissions.SAFE_METHODS
        is_authorized = user.is_teacher(school) or user.is_preceptor(school)
        
        if is_safe_method:
            if is_authorized:
                return True
        
        return user.is_directive(school)

    def has_object_permission(self, request, view, obj):
        """
        This method only checks if certain objects 
        (school, module, year, course, subject and event) 
        belong to the header school.
        """
        if isinstance(obj, CustomUser):
            return True
        
        school = request.school

        if school == obj:
            return True
        if hasattr(obj, 'school'):
            return obj.school == school
        if hasattr(obj, 'year'):
            return obj.year.school == school
        if hasattr(obj, 'course'):
            print(obj.course.year.school == school)
            return obj.course.year.school == school
        return False
                 