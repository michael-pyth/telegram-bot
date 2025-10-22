import requests, json, asyncio, config

HEADERS = {
    'X-Key': f'Key {config.API_KEY}',
    'X-Secret': f'Secret {config.SECRET_KEY}'
}

URL = 'https://api-key.fusionbrain.ai/'

def get_pipeline():
    response = requests.get(URL + 'key/api/v1/pipelines', headers=HEADERS)
    data = response.json()
    return data[0]['id']

async def generate(prompt, settings=None):
    default_params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "style": "DEFAULT",
        "generateParams": {
            "query": prompt
        }
    }

    if settings:
        default_params.update({
            "width": settings.get("width", 1024),
            "height": settings.get("height", 1024),
            "style": settings.get("style", "DEFAULT")
        })

    files = {
        'pipeline_id': (None, get_pipeline()),
        'params': (None, json.dumps(default_params), 'application/json')
    }

    response = requests.post(URL + 'key/api/v1/pipeline/run', headers=HEADERS, files=files)
    data = response.json()

    attempts = 0
    while attempts < 40:
        response = requests.get(URL + 'key/api/v1/pipeline/status/' + data['uuid'], headers=HEADERS)
        data = response.json()

        if data['status'] == 'DONE':
            return data['result']['files']

        attempts += 1
        await asyncio.sleep(3)
    raise TimeoutError("failed after 40 attempts")
