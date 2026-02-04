from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_items():
    return [{"item_id": 1, "name": "Example Item"}]

@router.post("/")
async def create_item(item: dict):
    return {"message": "Item created", "item": item}
