import boto3
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
)

# response = s3_client.put_object(
#     Bucket=settings.aws_s3_bucket,
#     Key="test/hello.txt",
#     Body=b"Hello from StockGuard"
# )

# print("S3 client berhasil dibuat")
# print(response)