from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.auth.service import verify_admin_token
from .crud import create_file_record, get_file_by_name
from fastapi.responses import Response

router = APIRouter(prefix="/admin/files", tags=["Admin Files"])


@router.post("/", dependencies=[Depends(verify_admin_token)])
async def upload_file(
        file: UploadFile = File(...),
        name: str = File(...),
        uploaded_by: str = "admin"
):
    try:
        file.filename = name

        return  await create_file_record(file, uploaded_by)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{name}", dependencies=[Depends(verify_admin_token)])
async def download_file(name: str):
    try:
        file_data = await get_file_by_name(name)

        return Response(
            content=file_data["content"],
            media_type=file_data["type"],
            headers={
                "Content-Disposition": f"attachment; filename={file_data['name']}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))