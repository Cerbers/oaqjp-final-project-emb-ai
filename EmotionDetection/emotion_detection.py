# URL: 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
# Headers: {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
# Input json: { "raw_document": { "text": text_to_analyze } }


import requests

def emotion_detector(text_to_analyze):
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    input_json = {
        "raw_document": {"text": text_to_analyze}
    }

    response = requests.post(url, headers=headers, json=input_json)

    if response.status_code == 200:
        data = response.json()

        try:
            emotion_dict = data['emotionPredictions'][0]['emotion']
        except (KeyError, IndexError, TypeError):
            return {"error": "Unexpected response structure from API"}

        emotions_scores = {
            'anger': emotion_dict.get('anger', 0),
            'disgust': emotion_dict.get('disgust', 0),
            'fear': emotion_dict.get('fear', 0),
            'joy': emotion_dict.get('joy', 0),
            'sadness': emotion_dict.get('sadness', 0)
        }

        sorted_emotions = sorted(emotions_scores.items(), key=lambda x: x[1], reverse=True)
        emotions_scores['dominant_emotion'] = sorted_emotions[0][0]

        return emotions_scores

    else:
        return {"error": f"Request failed with status code {response.status_code}"}