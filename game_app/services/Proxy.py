import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proxy_view(request):
    target_url = 'https://www.nexusmods.com/Core/Libs/Common/Managers/Downloads?GenerateDownloadUrl'
    
    headers = {
        'Origin': 'https://www.nexusmods.com',
        'Cookie': 'nexusmods_session=a062b51216543147955571ba031bba94; fwroute=1718180253.449.153.345433|b295758090068ae543818c1ba2aeea3e; nexusmods_session_refresh=1718186466; cf_clearance=gkKEewDuJju3tURyFWH224yo7HIIUv6Z4hIk3n8wDbo-1718188596-1.0.1.1-6b7uavZLeF_V4hx8ykEK9N9Aj1BlAdXswNAy1DWrsG9E8Re5HmnVcbR3Sz91oZtQA7wdsvSg64vePn4T2B1REA'
    }


    if request.method == 'POST':
        fid = request.POST.get('fid')
        game_id = request.POST.get('game_id')
        
        data = {
            'fid': fid,
            'game_id': game_id,
        }
        print(data)

        response = requests.post(target_url, headers=headers, data=data)
    else:
        return HttpResponse(status=405)

    print(response)

    return HttpResponse(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
