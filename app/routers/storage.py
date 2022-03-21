import logging
from os.path import isfile, join
import os
from http import HTTPStatus

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse


logger = logging.getLogger(__file__)
router = APIRouter(tags=['income'])

storage_path = 'my_storage'


@router.post('/create_file', status_code=HTTPStatus.OK)
async def create_file(filename: str, file_data: str):
    filename = join(storage_path, filename)
    with open(filename, 'w') as f:
        f.write(file_data)
    logger.info(f'Created file: {filename}')
    return {'Create': 'OK'}


@router.post('/delete_file', status_code=HTTPStatus.OK)
async def delete_file(filename: str) -> JSONResponse:
    filename = join(storage_path, filename)
    if isfile(filename):
        os.remove(filename)
        logger.info(f'Deleted file: {filename}')
        return JSONResponse({'Delete': 'OK'})
    else:
        logger.info(f'Delete failed: File does not exist ({filename})')
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='File not found')


@router.get('/download_file', status_code=HTTPStatus.OK, response_class=FileResponse)
async def download_file(filename: str) -> FileResponse:
    filename = join(storage_path, filename)
    if isfile(filename):
        logger.info(f'Downloaded file: {filename}')
        return FileResponse(filename)
    else:
        logger.info(f'Download failed: File does not exist ({filename})')
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='File not found')


@router.get('/list_files', status_code=HTTPStatus.OK, response_class=JSONResponse)
async def list_files() -> JSONResponse:
    files = os.listdir(storage_path)
    files = [f for f in files if isfile(join(storage_path, f))]
    logger.info(f'Listed files: {files}')
    return JSONResponse([{'files': files}])


@router.post('/upload_file', status_code=HTTPStatus.OK)
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:
    file_data = file.file.read()
    filename = join(storage_path, file.filename)
    with open(filename, 'wb') as f:
        f.write(file_data)
    logger.info(f'Uploaded file: {file.filename}')
    return JSONResponse({'Uploaded': 'OK'})
