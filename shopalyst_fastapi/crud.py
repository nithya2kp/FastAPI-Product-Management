from fastapi import  HTTPException
from schemas import ProductList,ProductDetail,ParentOrg
import requests
from typing import List
from config import BASE_PRODUCT_URL

import pandas as pd


def get_view_count(df: pd.DataFrame) -> ParentOrg:
    """
    List product view counts grouped by Parent Org and respective Brands.
     Parameters:
     -  df (pd.DataFrame): Excel data containing columns

    Returns:
        Custom ParentOrg response
    """
    expected_columns = {"Date", "Parent org", "Brand", "Product Id", "Product View Count"}
    if not expected_columns.issubset(df.columns):
        raise ValueError(f"Missing columns!!")

    parent_org_total = (
        df.groupby("Parent org")["Product View Count"]
        .sum()
        .sort_values(ascending=False)
    )

    result = []
    for parent, parent_count in parent_org_total.items():
        brands = (
            df[df["Parent org"] == parent]
            .groupby("Brand")["Product View Count"]
            .sum()
            .sort_values(ascending=False)
        )
        result.append({
            "parent_org": parent,
            "total_views": int(parent_count),
            "brands": [
                {"brand": brand, "views": int(count)}
                for brand, count in brands.items()
            ]
        })
    return result


def get_product_sku_details(product_id: str) -> ProductList:
    """
    List product and sub group details with skuId,shade,offerPrice: float,title
     Parameters:
     -  product_id: Respective product Id

    Returns:
        Custom ProductList response
    """
    response = requests.get(BASE_PRODUCT_URL.format(product_id=product_id))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Failed to fetch product {product_id} details!!")

    data = response.json()

    attr_values = data.get("attributeValues", [])
    title_dict = { item["id"]: item["title"] for item in attr_values }

    offer_price = data.get("offerPrice")
    if offer_price is None:
        raise HTTPException(status_code=500, detail="Missing OfferPrice!!")

    sku_details = data.get("skuSet", [])
    if not isinstance(sku_details, list):
        raise HTTPException(status_code=500, detail="Unexpected format!!")

    skus: List[ProductDetail] = []
    for sku in sku_details:
        shade_id = sku.get("attributes", {}).get("1")
        if shade_id is None:
            raise HTTPException(status_code=500,
                                detail="Missing shade attribute!!")
        title = title_dict.get(shade_id)
        if title is None:
            raise HTTPException(status_code=500,
                                detail=f"Title not available!!!")

        skus.append(
            ProductDetail(
                skuId=sku["skuId"],
                shade=shade_id,
                title=title,
                offerPrice=float(offer_price),
            )
        )

    return ProductList(productId=product_id, product_list=skus)
