import tensorflow as tf
from tensorflow.keras import layers, Model

def create_dummy_model():
    inputs = tf.keras.layers.Input(shape=(32,))
    x = tf.keras.layers.Dense(64, activation='relu')(inputs)
    x = tf.keras.layers.Dense(32, activation='relu')(x)
    model = Model(inputs=inputs, outputs=x)
    model.compile(loss= tf.losses.SparseCategoricalCrossentropy(), optimizer= tf.keras.optimizers.Adam(learning_rate=0.000001), metrics=['accuracy'])
    return model

