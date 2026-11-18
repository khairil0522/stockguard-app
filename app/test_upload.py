from app.services.storage_service import storage_service


# storage_service.upload_file(
#     file_content=b"Hello from Storage Service",
#     object_key="test/storage-service.txt",
#     content_type="text/plain",
# )

storage_service.delete(
    object_key="test/storage-service.txt"
)

# print("Upload berhasil")

print("Hapus berhasil")