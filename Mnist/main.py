import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
from PIL import Image

# Command to install tensorflow_datasets: pip install tensorflow-datasets
# Command to install tensorflow: pip install tensorflow

def normalize_img(image, label):
    return tf.cast(image, tf.float32) / 255., label

def train():
    (ds_train, ds_test), ds_info = tfds.load(
        'mnist',
        split=['train', 'test'],
        shuffle_files=True,
        as_supervised=True,
        with_info=True
        )
    
    ds_train =  ds_train.map(
        normalize_img, num_parallel_calls=tf.data.AUTOTUNE
    )
    ds_train = ds_train.cache()
    ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
    ds_train = ds_train.batch(128)
    ds_train = ds_train.prefetch(tf.data.AUTOTUNE)
        

    ds_test = ds_test.map(
        normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
    ds_test = ds_test.batch(128)
    ds_test = ds_test.cache()
    ds_test = ds_test.prefetch(tf.data.AUTOTUNE)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
    )

    model.fit(
        ds_train,
        epochs=6,
        validation_data=ds_test
    )
    
    model.save('mnist.h5')

def load():
    image = Image.open('image.png').convert('L')
    image_array = np.asarray(image) / 255.0
    image_array = np.reshape(image_array, (1, 28, 28, 1))
    model = tf.keras.models.load_model('mnist.h5')
    model.summary()
    prediction = model.predict(image_array)
    print(f'The model predicted: {np.argmax(prediction)}')

if __name__ == '__main__':
    load()  