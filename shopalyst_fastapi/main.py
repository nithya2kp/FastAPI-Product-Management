from fastapi import FastAPI,HTTPException
from fastapi import  File, UploadFile
from crud import get_view_count,get_product_sku_details
from schemas import ProductList,ParentOrg
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()


@app.post("/upload_excel",response_model=ParentOrg)
def upload_excel(file: UploadFile = File(...)):

    if file.content_type not in ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 "application/vnd.ms-excel"):
        raise HTTPException(status_code=400, detail="Invalid file type")
    try:
        df = pd.read_excel(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read Excel: {e}")
    try:
        count = get_view_count(df)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    return JSONResponse(content=count)


@app.get("/products/{product_id}/skudetail", response_model=ProductList)
def get_sku_details(product_id: str):
    return get_product_sku_details(product_id)