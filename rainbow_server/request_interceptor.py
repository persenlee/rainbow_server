from rest_framework.response import Response
from rest_framework import status
import hashlib


def request_interceptor_middleware(get_response):
    # One-time configuration and initialization.
    salt_str = '&*1@!￥8k@j@17U~a'

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        digest = request.META.get('HTTP_DIGEST')
        if digest is not None:
            params = {}
            if request.method == 'GET':
                params = request.GET
            elif request.method == 'POST':
                params = request.POST
            keys = sorted(params.keys())
            expr = ''
            for key in keys:
                expr += '{key}={value}&'.format(key=key, value=params.get(key, ''))
            expr += 'salt={}'.format(salt_str)
            encode_expr = expr.encode(encoding='UTF-8')
            md5 = hashlib.md5(encode_expr)
            hash_str = md5.hexdigest()
            if digest == hash_str:
                response = get_response(request)
                # Code to be executed for each request/response after
                # the view is called.
                return response
        return Response(status=status.HTTP_200_OK)

    return middleware
