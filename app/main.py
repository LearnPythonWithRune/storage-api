import logging
from http import HTTPStatus
from typing import Dict

from fastapi import FastAPI

from .routers import storage

logging.basicConfig(encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__file__)

app = FastAPI(
    title='Storage API',
    version='1.0.0',
    description='Store your files here',
    root_path=''
)

app.include_router(storage.router)


@app.get('/', status_code=HTTPStatus.OK)
async def root() -> Dict[str, str]:
    """
    Endpoint for basic connectivity test.
    """
    logger.info('root called')
    return {'message': 'I am alive'}
