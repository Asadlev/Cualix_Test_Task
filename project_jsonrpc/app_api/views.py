# myapp/views.py
import tempfile

from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from django.conf import settings


def api_call(request):
    result = None
    if request.method == 'POST':
        method = request.POST.get('method')
        params = request.POST.get('params', '{}')

        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            result = {'error': 'Invalid JSON in params'}
        else:
            data = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 1
            }

            headers = {'Content-Type': 'application/json'}
            url = "https://slb.medv.ru/api/v2/"

            # Создаем временные файлы для сертификата and ключа
            with tempfile.NamedTemporaryFile(delete=False) as cert_file, tempfile.NamedTemporaryFile(delete=False) as key_file:
                cert_file.write(settings.CERT.encode())
                cert_file.flush()
                key_file.write(settings.KEY.encode())
                key_file.flush()

                try:
                    response = requests.post(
                        url,
                        data=json.dumps(data),
                        headers=headers,
                        cert=(cert_file.name, key_file.name),
                        verify=True,
                    )
                    response_data = response.json()
                    result = response_data
                except requests.exceptions.RequestException as error:
                    result = {'error': str(error)}

    return render(request, 'api_form.html', {'result': result})
