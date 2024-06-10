from rest_framework import permissions
from rest_framework import exceptions
from .models import School, CustomUser


class SchoolHeader(permissions.BasePermission):
    MESSAGE_NOT_SCHOOL_ID = "Not provide school id in request headers."
    MESSAGE_SCHOOL_NOT_RECOGNIZED = "Unrecognized school."
    
    def has_permission(self, request, view):
        school_id = request.META.get('HTTP_SCHOOL_ID')
        print(school_id)
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
        
        if request.method in permissions.SAFE_METHODS:
            if user.is_teacher(school) or user.is_preceptor(school):
                return True

        if not user.is_directive(school):
            raise exceptions.PermissionDenied(self.MESSAGE_NOT_SCHOOL_DIRECTOR)
        
        return True

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
            
        