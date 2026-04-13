"""API module"""

from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/")
def home():
    """Render landing page."""
    return render_template('index.html')

@app.route("/emotionDetector")
def get_emotion_readout():
    """Call emotion_detection function to analyze user text."""

    text_to_analyze = request.args.get('textToAnalyze', '').strip()

    # Call the function (it now handles empty text internally)
    response = emotion_detector(text_to_analyze)

    # NEW: Check for None (blank input case)
    if response.get('dominant_emotion') is None:
        return "Invalid text! Please try again!"

    # Normal case - emotions detected
    anger = response['anger']
    disgust = response['disgust']
    fear = response['fear']
    joy = response['joy']
    sadness = response['sadness']
    dominant = response['dominant_emotion']

    output = (f"For the given statement, the system response is '{dominant}':\n"
              f"{anger}, 'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} "
              f"and 'sadness': {sadness}. The dominant emotion is {dominant}.")

    return output


if __name__ == "__main__":
    app.run(debug=True, port=5000)
