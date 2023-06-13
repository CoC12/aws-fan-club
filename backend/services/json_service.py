import json
import typing

decoder = json.JSONDecoder()


def extract_json(text: str) -> typing.Any:
    """
    JSON文字列を含む文字列から、JSON文字列を探しPythonオブジェクトを取得する。

    Args:
        text (str): JSON文字列を含む文字列

    Returns:
        typing.Any: Pythonオブジェクト

    Raises:
        ValueError: 文字列にJSONが含まれない場合
    """
    json_index = text.find('{')
    if json_index == -1:
        raise ValueError('JSON object not found')

    json_object, _ = decoder.raw_decode(text, json_index)
    return json_object
