from rest_framework.permissions import BasePermission


class IsOwnerUpdate(BasePermission):
	
	def has_permission(self, request, view):
		if request.method in ('PUT', 'PATCH'):
			pk = request.parser_context.get('kwargs')['pk']
			if request.user.is_authenticated and pk == str(request.user.id):
				return True
			return False
		return True
