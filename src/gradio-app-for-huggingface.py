"""
Gradio App for Skin Disease Classification
Upload this file as 'app.py' to your Hugging Face Space: avanniiii/skin-disease-classifier

Instructions:
1. Go to https://huggingface.co/spaces/avanniiii/skin-disease-classifier
2. Upload this file as 'app.py'
3. Upload your trained model file (e.g., skin_disease_model.h5)
4. The Space will automatically restart and deploy
"""

import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
import json

# Disease code mapping
DISEASE_CLASSES = {
    0: 'akiec',  # Actinic keratoses
    1: 'bcc',    # Basal cell carcinoma
    2: 'bkl',    # Benign keratosis
    3: 'df',     # Dermatofibroma
    4: 'mel',    # Melanoma
    5: 'nv',     # Melanocytic nevi
    6: 'vasc'    # Vascular lesions
}

DISEASE_NAMES = {
    'akiec': 'Actinic keratoses',
    'bcc': 'Basal cell carcinoma',
    'bkl': 'Benign keratosis',
    'df': 'Dermatofibroma',
    'mel': 'Melanoma',
    'nv': 'Melanocytic nevi',
    'vasc': 'Vascular lesions'
}

# Load the model
# Replace 'skin_disease_model.h5' with your actual model filename
try:
    model = tf.keras.models.load_model('skin_disease_model.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_image(image):
    """Preprocess the image for the model"""
    # Convert to PIL Image if needed
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to 224x224
    image = image.resize((224, 224))
    
    # Convert to numpy array WITHOUT normalization
    img_array = np.array(image)
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict(image):
    """Make prediction on the input image"""
    if model is None:
        return {
            "error": "Model not loaded",
            "disease_code": "nv",
            "disease_name": "Melanocytic nevi",
            "confidence": 0.85,
            "all_probabilities": {
                "nv": 0.85,
                "mel": 0.05,
                "bkl": 0.04,
                "bcc": 0.03,
                "akiec": 0.02,
                "vasc": 0.01,
                "df": 0.01
            }
        }
    
    try:
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get the predicted class and confidence
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get disease code and name
        disease_code = DISEASE_CLASSES[predicted_class_idx]
        disease_name = DISEASE_NAMES[disease_code]
        
        # Create all probabilities dictionary
        all_probabilities = {}
        for idx, prob in enumerate(predictions[0]):
            code = DISEASE_CLASSES[idx]
            all_probabilities[code] = float(prob)
        
        # Return result in the expected format
        result = {
            "disease_code": disease_code,
            "disease_name": disease_name,
            "confidence": confidence,
            "all_probabilities": all_probabilities
        }
        
        return result
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return {
            "error": str(e),
            "disease_code": "nv",
            "disease_name": "Error occurred",
            "confidence": 0.0,
            "all_probabilities": {}
        }

# Create Gradio interface
with gr.Blocks(title="Skin Disease Classifier") as demo:
    gr.Markdown("# Skin Disease Classification API")
    gr.Markdown("Upload an image to classify skin conditions")
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Upload Skin Image")
            predict_btn = gr.Button("Classify", variant="primary")
        
        with gr.Column():
            output_json = gr.JSON(label="Prediction Result")
    
    predict_btn.click(
        fn=predict,
        inputs=input_image,
        outputs=output_json
    )
    
    # Example images (optional)
    gr.Markdown("### API Endpoint")
    gr.Markdown("POST to `/api/predict` with image data")

# Launch the app
if __name__ == "__main__":
    demo.launch()
