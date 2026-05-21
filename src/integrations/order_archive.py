import json
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError

from src.models import Order, OrderItem
from src.schemas.config import get_settings


def decimal_to_string(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), "f")


def serialize_order_item(item: OrderItem) -> dict[str, object]:
    return {
        "menu_item_id": item.menu_item_id,
        "quantity": item.quantity,
        "extras": item.extras,
        "unit_price": decimal_to_string(item.unit_price),
        "line_total": decimal_to_string(item.line_total),
    }


def build_order_summary(order: Order) -> dict[str, object]:
    return {
        "order_id": order.id,
        "customer_name": order.customer_name,
        "status": order.status,
        "subtotal": decimal_to_string(order.subtotal),
        "discount_amount": decimal_to_string(order.discount_amount),
        "total_price": decimal_to_string(order.total_price),
        "coupon_code": order.coupon_code,
        "created_at": order.created_at.isoformat(),
        "items": [serialize_order_item(item) for item in order.items],
    }


def create_s3_client():
    settings = get_settings()
    return boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        endpoint_url=settings.aws_endpoint_url,
    )


def bucket_exists(s3_client, bucket_name: str) -> bool:
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False


def ensure_bucket_exists(s3_client, bucket_name: str) -> None:
    if bucket_exists(s3_client, bucket_name):
        return
    settings = get_settings()
    if settings.aws_region == "us-east-1":
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": settings.aws_region},
        )


def archive_order_summary(order: Order) -> None:
    settings = get_settings()
    s3_client = create_s3_client()
    ensure_bucket_exists(s3_client, settings.s3_bucket_name)
    s3_client.put_object(
        Bucket=settings.s3_bucket_name,
        Key=f"orders/{order.id}.json",
        Body=json.dumps(build_order_summary(order)).encode("utf-8"),
        ContentType="application/json",
    )
