from app.core.awss3 import s3_client
from app.core.config import settings

class StorageService:

    def upload(self, file_content: bytes, object_key: str, content_type: str):
        return s3_client.put_object(
            Bucket=settings.aws_s3_bucket,
            Key=object_key,
            Body=file_content,
            ContentType=content_type,
        )

    def delete(self, object_key: str):
        return s3_client.delete_object(
            Bucket=settings.aws_s3_bucket,
            Key=object_key,
        )

    def generate_presigned_url(self, object_key: str, expiration: int = 3600):
        return s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.aws_s3_bucket,
                "Key": object_key,
            },
            ExpiresIn=expiration,
        )

storage_service = StorageService()