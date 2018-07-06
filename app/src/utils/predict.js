import * as tf from '@tensorflow/tfjs';

export default async (data, useScikitLearn) => {
    if (useScikitLearn) {
        return fetch('http://0.0.0.0:5000/predict', {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(data)
        }).then((res) => res.json())
    } else {
        const model = await tf.loadModel("http://localhost:3000/tf_js_model/model.json");
        const { locations, specs: { no_bed, no_toilets, no_bath } } = data;

        let tensors = locations.map((A, i) => {
          return tf.tensor2d([[A.lng, A.lat, Number(no_bed), Number(no_toilets), Number(no_bath)]]);
        });

        const predictions = tensors.map(T => model.predict(T).asScalar().data());
        
        return await Promise.all(predictions)
            .then((prices) => ({ prices }));
    }
}