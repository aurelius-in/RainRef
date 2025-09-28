import os
from typing import Optional

try:
    from azure.storage.blob import BlobServiceClient  # type: ignore
except Exception:  # pragma: no cover
    BlobServiceClient = None  # type: ignore


def _get_conn_str() -> Optional[str]:
    return os.getenv("BLOB_CONN_STRING") or os.getenv("AZURE_BLOB_CONN_STRING")


def upload_bytes(container: str, blob_name: str, data: bytes, content_type: str = "application/octet-stream") -> str:
    conn = _get_conn_str()
    if BlobServiceClient and conn:
        try:
            svc = BlobServiceClient.from_connection_string(conn)
            container_client = svc.get_container_client(container)
            try:
                container_client.create_container()
            except Exception:
                pass
            container_client.upload_blob(name=blob_name, data=data, overwrite=True, content_settings={"content_type": content_type})
            account_url = svc.url if hasattr(svc, "url") else ""
            return f"{account_url}/{container}/{blob_name}".rstrip("/")
        except Exception:
            pass
    # fallback: local file storage
    os.makedirs("tmp_uploads", exist_ok=True)
    path = os.path.join("tmp_uploads", blob_name)
    with open(path, "wb") as f:
        f.write(data)
    return f"file://{os.path.abspath(path)}"
