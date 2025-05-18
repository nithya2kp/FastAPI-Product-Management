from pydantic import BaseModel
from typing import List

class Brand(BaseModel):
    brand: str
    views: int


class ParentOrg(BaseModel):
    parent_org: str
    total_views: int
    brands: List[Brand]
    
class ProductDetail(BaseModel):
    skuId: str
    shade: str
    offerPrice: float
    title: str

class ProductList(BaseModel):
    productId: str
    product_list: List[ProductDetail]