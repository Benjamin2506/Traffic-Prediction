from tensorflow.keras.models import load_model
model = load_model('model.h5')
def predict_time(distance, speed, vehicle_type):
    # Implement your prediction model logic here
    # For demonstration, we'll use a simple calculation
    predicted_time = model.predict(duration)  # in minutes
    return predicted_time
