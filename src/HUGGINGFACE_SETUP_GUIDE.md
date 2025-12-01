# Hugging Face Space Setup Guide for SkinCare AI

This guide will help you deploy your skin disease classification model to Hugging Face Spaces so the SkinCare AI app can connect to your real ML model.

## 📋 Prerequisites

- Your trained TensorFlow/Keras model file (`.h5` format)
- A Hugging Face account (free): https://huggingface.co/join

## 🚀 Step-by-Step Setup

### Step 1: Access Your Hugging Face Space

1. Go to: https://huggingface.co/spaces/avanniiii/skin-disease-classifier
2. Click "Sign In" if you haven't already
3. If the space doesn't exist, create it:
   - Go to https://huggingface.co/new-space
   - Name: `skin-disease-classifier`
   - License: `apache-2.0`
   - SDK: `gradio`
   - Click "Create Space"

### Step 2: Upload Your Files

You need to upload 2 files to your Space:

#### File 1: `app.py`
Copy the contents from `/gradio-app-for-huggingface.py` in this project.

1. In your Space, click "Files" → "Add file" → "Create a new file"
2. Name it: `app.py`
3. Copy the ENTIRE contents from the `gradio-app-for-huggingface.py` file
4. Click "Commit new file to main"

#### File 2: Your Model File
Upload your trained model (e.g., `skin_disease_model.h5`)

1. Click "Files" → "Add file" → "Upload files"
2. Upload your `.h5` model file
3. Make sure the filename matches what's in `app.py` (line 36)
   - If your model has a different name, update line 36 in app.py:
     ```python
     model = tf.keras.models.load_model('YOUR_MODEL_FILENAME.h5')
     ```
4. Click "Commit to main"

### Step 3: Wait for Deployment

1. The Space will automatically start building
2. You'll see a "Building" status at the top
3. Wait 2-5 minutes for it to complete
4. Once done, you'll see "Running" status

### Step 4: Test Your Space

1. You should see a Gradio interface in your Space
2. Upload a test skin image
3. Click "Classify"
4. You should get a JSON response with:
   ```json
   {
     "disease_code": "nv",
     "disease_name": "Melanocytic nevi",
     "confidence": 0.87,
     "all_probabilities": {...}
   }
   ```

### Step 5: Verify API Connection

1. Go back to your SkinCare AI app
2. Sign in (use demo account: `demo@skincare.ai` / `demo123456`)
3. Upload a skin image and analyze it
4. Check the browser console (F12) for logs
5. You should see: `Success with endpoint: https://avanniiii-skin-disease-classifier.hf.space/call/predict`

## 🔧 Troubleshooting

### Problem: Space shows "Build Error"

**Solution:** Check the logs in your Space. Common issues:
- Missing dependencies in requirements.txt
- Model file not found (check filename matches in app.py)
- TensorFlow version incompatibility

Add a `requirements.txt` file with:
```
gradio
tensorflow
pillow
numpy
```

### Problem: API still returns mock data

**Solution:**
1. Check that your Space status is "Running" (not "Building" or "Sleeping")
2. Verify the Space URL is correct: `https://avanniiii-skin-disease-classifier.hf.space`
3. Check browser console for detailed error messages
4. Make sure your model file is correctly uploaded

### Problem: Model predictions are wrong

**Solution:**
1. Verify the disease class mapping in app.py (lines 14-21) matches your model's training
2. Update the `DISEASE_CLASSES` dictionary to match your model's output indices
3. Ensure image preprocessing matches your training pipeline (224x224, normalized to 0-1)

## 📝 Model Requirements

Your model should:
- Accept input shape: (None, 224, 224, 3)
- Output 7 classes in this order:
  0. akiec (Actinic keratoses)
  1. bcc (Basal cell carcinoma)
  2. bkl (Benign keratosis)
  3. df (Dermatofibroma)
  4. mel (Melanoma)
  5. nv (Melanocytic nevi)
  6. vasc (Vascular lesions)

If your model uses different class order, update the `DISEASE_CLASSES` dictionary in app.py.

## ✅ Success Checklist

- [ ] Hugging Face Space is created
- [ ] app.py is uploaded and committed
- [ ] Model file (.h5) is uploaded and committed
- [ ] Space status shows "Running"
- [ ] Test image classification works in the Gradio interface
- [ ] SkinCare AI app connects successfully (no mock data warning)
- [ ] Predictions are accurate and meaningful

## 🆘 Need Help?

If you're still having issues:

1. **Check Space Logs:** Click "Logs" in your Hugging Face Space
2. **Check Browser Console:** Press F12 in your browser to see detailed error messages
3. **Verify Model:** Make sure your model file is valid and can be loaded with:
   ```python
   import tensorflow as tf
   model = tf.keras.models.load_model('your_model.h5')
   print(model.summary())
   ```

## 🎉 What's Next?

Once your Space is running:
- The app will automatically use your real ML model
- No code changes needed in the SkinCare AI app
- Users will get real predictions instead of mock data
- You can update your model anytime by uploading a new .h5 file to the Space

---

**Note:** While your Space is being set up, the app will intelligently fall back to mock predictions so users can still test the interface. This is normal and expected!
