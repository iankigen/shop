def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FOWARDED_FOR')
	return x_forwarded_for.slit(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
