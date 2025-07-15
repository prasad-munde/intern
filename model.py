import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import sys
from keras.layers import TFSMLayer

# Image path argument
image_path = sys.argv[1] if len(sys.argv) > 1 else "fliphome.png"

# Load class labels
with open("labels.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# Load the SavedModel using TFSMLayer (Keras 3+)
model = TFSMLayer("model.savedmodel", call_endpoint="serving_default")

# Preprocess the image
image = Image.open(image_path).convert("RGB")
image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
image_array = np.asarray(image).astype(np.float32)
normalized = (image_array / 127.5) - 1.0
input_tensor = np.expand_dims(normalized, axis=0)

# Inference
output = model(input_tensor)

# Handle dictionary output
if isinstance(output, dict):
    print("\nOutput keys:", list(output.keys()))
    # Get the tensor from dict
    prediction = list(output.values())[0].numpy()
else:
    prediction = output.numpy()

# Get top prediction
index = np.argmax(prediction)
confidence = prediction[0][index]

# Output result
print(f"\n Page Type: {class_names[index]}")
print(f"Confidence: {confidence * 100:.2f}%")
