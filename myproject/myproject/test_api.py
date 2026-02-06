from django.conf import settings
from django.core.management import call_command
from ninja import Router, Schema
from ninja.responses import Response

router = Router()


class ResetDbResponse(Schema):
    success: bool
    message: str


@router.post("/reset-db", response=ResetDbResponse)
def reset_db(request):
    """E2Eテスト用: DBをリセットして初期データを投入"""
    # 本番環境では403を返す
    if not settings.DEBUG:
        return Response(
            {"success": False, "message": "This endpoint is only available in DEBUG mode"},
            status=403,
        )

    try:
        call_command("flush", "--no-input")
        call_command("loaddata", "initial_data.json")
        return {"success": True, "message": "Database reset successfully"}
    except Exception as e:
        return Response(
            {"success": False, "message": f"Reset failed: {str(e)}"},
            status=500,
        )
