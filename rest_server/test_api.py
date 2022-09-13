from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse
from rest_server.api_schema import SampleInput

# Create fast API router
router = APIRouter()


@router.post(
    path="/sample",
    tags=["Sample"],
)
async def sample_api(
    request: Request,
    data: SampleInput,
):
    """
    Sample API
    """
    await request.app.logger.info("Sample API call")
    return JSONResponse(data.dict())
