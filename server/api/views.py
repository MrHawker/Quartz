
from django.http import JsonResponse
from django.utils.timezone import now
from .ibm_runtime import get_ibm_runtime

def health(req):
    return JsonResponse({"ok": True, "time": now().isoformat()})

def backends(req):
    ibm_run_time_service = get_ibm_runtime()
    data = ibm_run_time_service.list_backends()
    if isinstance(data, dict) and data.get("error"):
        return JsonResponse(data, status=data.get("status", 502))
    return JsonResponse(data, safe=not isinstance(data, list))