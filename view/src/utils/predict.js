export default async (data) => {
    return fetch('/predict', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(data)
    }).then((res) => res.json())
}