import os
import requests

def token(request):
    if not "Authorization" in request.headers:  # Word Authorization missing from the request header
        return None, ("Missing credentials", 401)
    
    token = request.headers["Authorization"]

    if not token:  # If token is missing
        return None, ("Missing credentials", 401)
    
    resposne = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},        
    )

    if resposne.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


