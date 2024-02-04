export async function discogSendVerifier(verifier) {
    try {
        console.log({"verifier": verifier});
        const user = JSON.parse(localStorage.getItem('user'))
        let headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        headers['Authorization'] = 'Bearer ' + user.data

        const result = await fetch("http://127.0.0.1:5001/discog/verifier", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({"verifier": verifier}),
        })
        return result.json().then(data => {
            return data
        })
    }
    catch (e) {
        console.log(e)
    }
}

export async function discogConnect() {
    // send request to localhost:3000/api/discogs to get the access token
    console.log("hello")
    const result = await fetch("http://127.0.0.1:5001/discog", {
        method: "GET",
    }).then(response => {
        response.json().then(data => {
            console.log(data)
            if(data['token']) {
                window.location.href = data['token']
            }
        })
        }
    );
}
