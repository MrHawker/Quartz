import requests
import time
from django.conf import settings

## Return this if the server already instantiate a ibm runtime client
existing_ibm_run_time = None

class IBM_RUNTIME():
    def __init__(self):
        self._IBM_CLOUD_API_KEY = settings.IBM_CLOUD_API_KEY
        self._IBM_IAM_URL = settings.IBM_IAM_URL
        self._IBM_HTTP_TIMEOUT = float(settings.IBM_HTTP_TIMEOUT)
        self._safety_margin = int(settings.IBM_TOKEN_SAFETY_MARGIN)
        # PLS ONLY ACCESS THE TOKEN THROUGH THE _GET_TOKEN PRIVATE FUNC
        # This is because the token expires in about 1 hour and the mechanism for caching the token and refetching is built into the get token function
        self._bearer_token = None
        self._expiration = 0
        self._crn_instance = settings.IBM_QUANTUM_INSTANCE_CRN
        self._base_url = settings.IBM_BASE_URL

    def _should_refresh(self) -> bool:
        # print("--------------------------------")
        # print(self._expiration)
        # print(int(time.time()) + self._safety_margin)
        # print("--------------------------------")
        if not self._bearer_token or int(time.time()) + self._safety_margin >= self._expiration:
            return True
        return False

    def _get_bearer_token_from_ibm(self):
        if not self._IBM_CLOUD_API_KEY:
            raise RuntimeError("IBM_CLOUD_API_KEY not found")
        
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self._IBM_CLOUD_API_KEY,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(self._IBM_IAM_URL,data,headers= headers,timeout=self._IBM_HTTP_TIMEOUT)

        response_json = response.json()

        print("Received: \n",response_json)

        self._bearer_token = response_json["access_token"]

        self._expiration = int(response_json["expiration"])

    def _get_token(self):
        if self._should_refresh():
            self._get_bearer_token_from_ibm()
        return self._bearer_token
    
    # Print available backend ig
    def list_backends(self) -> dict:
        BACKEND_URL = f"{self._base_url}/api/v1/backends"

        if not self._crn_instance:
            raise RuntimeError("IBM_QUANTUM_INSTANCE_CRN not set")

        bearer_token = self._get_token()

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
            "Service-CRN": self._crn_instance,
        }
        message_dict = None
        try:
            response = requests.get(BACKEND_URL,headers=headers,timeout=self._IBM_HTTP_TIMEOUT)
            if response.status_code in (401,403):
                message_dict = {
                    "status": "ERROR",
                    "status_code": response.status_code,
                    "message": "Auth failed."
                }
            else:
                message_dict = response.json()
        except:
            message_dict =  {
                "status": "ERROR",
                "status_code": response.status_code,
                "message": "Something went wrong. Please let me know at caovongan1922@gmail.com"
            }

        print(message_dict)

        return message_dict


def get_ibm_runtime() -> IBM_RUNTIME:
    global existing_ibm_run_time
    if existing_ibm_run_time is None:
        existing_ibm_run_time = IBM_RUNTIME()
    return existing_ibm_run_time