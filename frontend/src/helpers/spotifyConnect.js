import useFetch from "./hooks/useFetch";
import {URL_SPOTIFY} from "../config/config";
import {useEffect} from "react";

const clientId = "300cdf3993c94b429d91a6e4338a5aa7"; // Replace with your client ID
const params = new URLSearchParams(window.location.search);
const code = params.get("code");

// export function sendToken(access_token) {
//     const data_conn = { access_token: access_token };
//     const {fetch_data, isPending, data} = useFetch(URL_SPOTIFY, 'POST', {
//         needs_auth:false,
//         immediate:false,
//         data: [data_conn]
//     })
//     useEffect(() => {
//         // This effect will be called when the component using useTokenSender mounts or when access_token changes
//         fetch_data(); // You may need to adjust this based on your useFetch implementation
//     }, [access_token, fetch_data]);
//
//     return { isPending, data };
// }
export async function spotifyConnect() {

    if (!code) {
        await redirectToAuthCodeFlow(clientId);
    } else {
        const accessToken = await getAccessToken(clientId, code);
        // const profile = await fetchProfile(accessToken);
        // sendToken(accessToken);
        console.log(accessToken)
        console.log("hello");
    }
}

export async function redirectToAuthCodeFlow(clientId) {
    const verifier = generateCodeVerifier(128);
    const challenge = await generateCodeChallenge(verifier);

    localStorage.setItem("verifier", verifier);

    const params = new URLSearchParams();
    params.append("client_id", clientId);
    params.append("response_type", "code");
    params.append("redirect_uri", "http://localhost:3000/friends");
    params.append("scope", "user-read-private user-read-email");
    params.append("code_challenge_method", "S256");
    params.append("code_challenge", challenge);

    document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
}

function generateCodeVerifier(length) {
    let text = '';
    let possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    for (let i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

async function generateCodeChallenge(codeVerifier) {
    const data = new TextEncoder().encode(codeVerifier);
    const digest = await window.crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode.apply(null, [...new Uint8Array(digest)]))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}
export async function getAccessToken(clientId, code) {
    const verifier = localStorage.getItem("verifier");

    const params = new URLSearchParams();
    params.append("client_id", clientId);
    params.append("grant_type", "authorization_code");
    params.append("code", code);
    params.append("redirect_uri", "http://localhost:3000/friends");
    params.append("code_verifier", verifier);

    const result = await fetch("https://accounts.spotify.com/api/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params
    });

    const { access_token } = await result.json();
    console.log("access token")
    console.log(access_token)
    return access_token;
}

async function fetchProfile(token) {
    const result = await fetch("https://api.spotify.com/v1/me", {
        method: "GET", headers: { Authorization: `Bearer ${token}` }
    });
    const data = await result.json();
    console.log(data)

    const result_playlist = await fetch("", {
        method: "GET", headers: { Authorization: `Bearer ${token}` }
    });
    const data_playlist = await result_playlist.json();
    console.log(data_playlist)

    const result_playlist_tracks = await fetch(`https://api.spotify.com/v1/playlists/${data_playlist['items'][0]['id']}/tracks`, {
        method: "GET", headers: { Authorization: `Bearer ${token}` }
    });
    const data_playlist_track = await result_playlist_tracks.json();
    console.log(data_playlist_track)
    return data;
}