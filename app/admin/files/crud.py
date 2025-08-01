from datetime import datetime

import boto3
import os
from botocore.exceptions import ClientError
from app.pg_db import files, database
from typing import Dict, Optional
import uuid

class MinioClient:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=os.getenv('MINIO_ENDPOINT', 'http://localhost:9000'),
            aws_access_key_id=os.getenv('MINIO_ACCESS_KEY', 'admin'),
            aws_secret_access_key=os.getenv('MINIO_SECRET_KEY', 'standartpass'),
            region_name='us-east-1'
        )
        self.ensure_bucket()

    def ensure_bucket(self):
        try:
            self.client.head_bucket(Bucket='product-images')
        except ClientError:
            self.client.create_bucket(Bucket='product-images')

    def upload_file(self, file_data) -> str:
        try:
            object_key = f"files/{file_data.filename}"
            file_data.file.seek(0)
            self.client.upload_fileobj(file_data.file, 'product-images', object_key)
            return object_key
        except ClientError as e:
            raise Exception(f"Upload failed: {str(e)}")
        finally:
            file_data.file.close()

    def get_file(self, object_key: str):
        try:
            response = self.client.get_object(Bucket='product-images', Key=object_key)
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"Download failed: {str(e)}")

minio_client = MinioClient()

async def create_file_record(file_data, uploaded_by: str) -> Dict[str, any]:
    try:
        file_data.file.seek(0, os.SEEK_END)
        weight_kb = file_data.file.tell() / 1024
        file_data.file.seek(0)
        object_key = minio_client.upload_file(file_data)

        query = files.insert().values(
            uuid=str(uuid.uuid4()),
            name=file_data.filename,
            type=file_data.content_type,
            weight=weight_kb,
            uploaded_by=uploaded_by,
            uploaded_at=datetime.utcnow(),
            status='active'
        )
        await database.execute(query)
        return {"message": "Success"}

    except Exception as e:
        raise Exception(f"Failed to create file record: {str(e)}")


async def get_file_by_name(name: str) -> Optional[Dict[str, any]]:
    try:
        query = files.select().where(files.c.name == name)
        result = await database.fetch_one(query)
        if not result:
            raise Exception("File not found")
        content = minio_client.get_file(f"files/{name}")
        return {
            "uuid": result['uuid'],
            "name": result['name'],
            "type": result['type'],
            "weight": result['weight'],
            "content": content
        }
    except Exception as e:
        raise Exception(f"Failed to retrieve file: {str(e)}")