from fastapi import APIRouter

router = APIRouter(prefix="/health", include_in_schema=False)


@router.get("")
async def health_check():
    return {"health": "OK"}
