"""
AI-Based Crop Disease Detection System
Perfect for Nepal Agriculture Context
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from PIL import Image
import os

# Disease information database
DISEASE_INFO = {
    'healthy': {
        'treatment': 'No treatment needed. Continue regular care.',
        'prevention': 'Maintain good watering and sunlight.'
    },
    'bacterial_blight': {
        'treatment': 'Remove infected leaves. Apply copper-based fungicide. Improve air circulation.',
        'prevention': 'Avoid overhead watering. Use disease-free seeds.'
    },
    'leaf_spot': {
        'treatment': 'Remove affected leaves. Apply neem oil or fungicide. Reduce humidity.',
        'prevention': 'Space plants properly. Water at base of plants.'
    },
    'rust': {
        'treatment': 'Apply sulfur-based fungicide. Remove infected parts. Improve drainage.',
        'prevention': 'Ensure good air flow. Avoid wetting leaves.'
    },
    'powdery_mildew': {
        'treatment': 'Spray with baking soda solution (1 tbsp per liter). Apply neem oil.',
        'prevention': 'Provide adequate spacing. Ensure sunlight reaches leaves.'
    }
}

class CropDiseaseDetector:
    def __init__(self, img_size=150):
        self.img_size = img_size
        self.model = None
        self.class_names = ['healthy', 'bacterial_blight', 'leaf_spot', 'rust', 'powdery_mildew']
        
    def build_model(self):
        """Build a simple CNN model for disease detection"""
        model = keras.Sequential([
            # Input layer
            layers.Input(shape=(self.img_size, self.img_size, 3)),
            
            # Rescaling
            layers.Rescaling(1./255),
            
            # Convolutional layers
            layers.Conv2D(32, 3, activation='relu'),
            layers.MaxPooling2D(),
            
            layers.Conv2D(64, 3, activation='relu'),
            layers.MaxPooling2D(),
            
            layers.Conv2D(128, 3, activation='relu'),
            layers.MaxPooling2D(),
            
            # Dense layers
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def train_model(self, train_dir, epochs=10):
        """Train the model on your dataset"""
        # Load training data
        train_ds = keras.preprocessing.image_dataset_from_directory(
            train_dir,
            image_size=(self.img_size, self.img_size),
            batch_size=32
        )
        
        # Train
        history = self.model.fit(train_ds, epochs=epochs)
        return history
    
    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        img = Image.open(image_path)
        img = img.resize((self.img_size, self.img_size))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, 0)  # Add batch dimension
        return img_array
    
    def predict_disease(self, image_path):
        """Predict disease from leaf image"""
        if self.model is None:
            raise Exception("Model not built or loaded. Call build_model() first.")
        
        # Preprocess image
        img_array = self.preprocess_image(image_path)
        
        # Make prediction
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class]
        
        disease_name = self.class_names[predicted_class]
        
        return {
            'disease': disease_name,
            'confidence': float(confidence),
            'all_predictions': {
                self.class_names[i]: float(predictions[0][i]) 
                for i in range(len(self.class_names))
            }
        }
    
    def get_treatment(self, disease_name):
        """Get treatment recommendation"""
        return DISEASE_INFO.get(disease_name, {
            'treatment': 'Consult agricultural expert.',
            'prevention': 'Follow good farming practices.'
        })
    
    def diagnose(self, image_path):
        """Complete diagnosis with treatment"""
        result = self.predict_disease(image_path)
        treatment = self.get_treatment(result['disease'])
        
        return {
            **result,
            'treatment': treatment['treatment'],
            'prevention': treatment['prevention']
        }
    
    def save_model(self, path='crop_disease_model.h5'):
        """Save trained model"""
        self.model.save(path)
        print(f"Model saved to {path}")
    
    def load_model(self, path='crop_disease_model.h5'):
        """Load pretrained model"""
        self.model = keras.models.load_model(path)
        print(f"Model loaded from {path}")


# Example Usage
def main():
    print("🌾 Crop Disease Detection System for Nepal Agriculture 🌾\n")
    
    # Initialize detector
    detector = CropDiseaseDetector()
    
    # Build model
    print("Building CNN model...")
    detector.build_model()
    print(f"Model built successfully!\n")
    
    # For training (if you have dataset):
    # Organize your images in folders like:
    # train_data/
    #   ├── healthy/
    #   ├── bacterial_blight/
    #   ├── leaf_spot/
    #   ├── rust/
    #   └── powdery_mildew/
    
    # Uncomment to train:
    # detector.train_model('train_data', epochs=10)
    # detector.save_model()
    
    # For prediction (example):
    print("=" * 60)
    print("To use this system:")
    print("1. Collect leaf images of healthy and diseased crops")
    print("2. Organize them in folders by disease type")
    print("3. Train the model using train_model()")
    print("4. Use diagnose() to detect diseases in new images")
    print("=" * 60)
    
    # Example prediction (after training):
    # result = detector.diagnose('test_leaf.jpg')
    # print(f"\n🔍 Disease Detected: {result['disease'].upper()}")
    # print(f"📊 Confidence: {result['confidence']*100:.2f}%")
    # print(f"\n💊 Treatment: {result['treatment']}")
    # print(f"🛡️ Prevention: {result['prevention']}")


if __name__ == "__main__":
    main()


# Quick Start Guide for Nepali Farmers:
"""
स्टेप १: तस्बीर संकलन (Collect Images)
- स्वस्थ पातहरु (Healthy leaves)
- बिरामी पातहरु (Diseased leaves)

स्टेप २: मोडेल तालिम (Train Model)
detector = CropDiseaseDetector()
detector.build_model()
detector.train_model('train_data', epochs=10)
detector.save_model()

स्टेप ३: रोग पत्ता लगाउनुहोस् (Detect Disease)
result = detector.diagnose('leaf_photo.jpg')
print(result)
"""