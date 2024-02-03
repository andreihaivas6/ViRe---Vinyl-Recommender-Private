import useFetch from "./hooks/useFetch";
import {API_URL, PLAYLIST_PORT, URL_SPOTIFY} from "../config/config";
import React, {useEffect, useState} from 'react';
import {icons, swal} from "./mySwal";

const clientId = "300cdf3993c94b429d91a6e4338a5aa7"; // Replace with your client ID
const params = new URLSearchParams(window.location.search);
const code = params.get("code");

export async function UseSentToken(accessToken) {
    const data_conn = { access_token: accessToken }
    const result = await fetch(API_URL + PLAYLIST_PORT + URL_SPOTIFY + "/" + accessToken, {
        method: 'POST',
        body: JSON.stringify(data_conn),
    })
    // setStatus(result.status)
    const data_json = await result.json()

    return { data: data_json};
}

export async function spotifyConnect() {

    if (!code) {
        await redirectToAuthCodeFlow(clientId);
    } else {
        const accessToken = await getAccessToken(clientId, code);
        return await UseSentToken(accessToken);
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

    const { access_token } =  await result.json().then(data => {
        console.log("hsllo: ",data)

        return data;

    });
    return await access_token;
}