# authentication/permissions.py
from rest_framework import permissions

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'EMPLOYEE'
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE'] and hasattr(obj, 'employee_id'):
            return False
        return obj.employee_id == request.user.employee_id

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'MANAGER'
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'employee_id') and obj.employee_id == request.user.employee_id:
            return request.method != 'DELETE'
        return obj.manager_id == request.user.employee_id

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return request.user and request.user.role == 'ADMIN'