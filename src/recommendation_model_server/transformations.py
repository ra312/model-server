from typing import Any, List


def to_frontend_suggestions(es_response: Any) -> List[Any]:
    result = []

    if es_response and "suggest" in es_response and "autocomplete" in es_response["suggest"]:
        if es_response["suggest"].get("autocomplete", []):
            suggestions = es_response["suggest"]["autocomplete"][0]
            for each in suggestions.get("options", []):
                result.append(each["text"])

    return result


def to_frontend_results(es_response: Any) -> List[Any]:
    result = []

    if es_response and "hits" in es_response:
        for each in es_response["hits"].get("hits", []):
            restaurant = each["_source"]
            document = {
                "id": restaurant["venue"]["id"],
                "image": restaurant["image"]["url"],
                "url": f'https://wolt.com/en/deu/berlin/restaurant/{restaurant["venue"]["slug"]}',
                "title": restaurant["venue"]["name"],
                "subtitle": restaurant["venue"]["short_description"],
                "rating": "😅",
            }

            if "rating" in restaurant["venue"]:
                if restaurant["venue"]["rating"]["score"] >= 9.0:
                    document["rating"] = "😁"
                elif restaurant["venue"]["rating"]["score"] >= 7.0:
                    document["rating"] = "🙂"
                else:
                    document["rating"] = "😐"

            result.append(document)

    return result
