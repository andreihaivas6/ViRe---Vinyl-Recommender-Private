// https://www.bezkoder.com/react-hooks-redux-login-registration-example/

import { useEffect, useState } from 'react';
import jwt_decode from "jwt-decode";
import axios from "axios";
import { useNavigate } from "react-router-dom"

import { API_URL, API_URL_PLAYLIST, API_URL_USER, API_URL_RECOMMENDATION, API_URL_SPARQL, URL_REFRESH, USER_PORT, PLAYLIST_PORT, RECOMMENDATION_PORT, SPARQL_PORT } from '../../config/config';
import { swal, icons } from '../mySwal';

export default function useFetch(service_port, url, method_name, {
        given_body=null, 
        needs_auth=true,
        immediate=true,
    }) {
    const [isPending, setIsPending] = useState(true)
    const [data, setData] = useState([])
    const [error, setError] = useState() 
    const [status, setStatus] = useState(0)

    const navigation = useNavigate();
    
    let api_url = 0
    if (service_port === USER_PORT) {
        api_url = API_URL_USER
    } else if (service_port === PLAYLIST_PORT) {
        api_url = API_URL_PLAYLIST
    } else if (service_port === RECOMMENDATION_PORT) {
        api_url = API_URL_RECOMMENDATION
    } else if (service_port === SPARQL_PORT) {
        api_url = API_URL_SPARQL
    }
    let complete_url = api_url + service_port + url
    // console.log(complete_url)

    const fetch_data = (async () => {
        let headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        try {

            headers = needs_auth ? await getAuth(headers, navigation) : headers

            const result = await fetch(complete_url, {
                method: method_name,
                body: given_body != null ? JSON.stringify(given_body) : null,
                headers: headers,
            })
            setStatus(result.status)
            const data_json = await result.json()

            setData(data_json)
            setIsPending(false)
        }
        catch(_error) {
            setError(_error) 
            setIsPending(false)
        }
    })

    useEffect(() => {
        immediate && fetch_data()
    }, [])

    return {
        fetch_data,
        isPending, 
        data, 
        error,
        status
    }
}

async function getAuth(headers, navigation) {
    const user = JSON.parse(localStorage.getItem('user'))

    if (user && user.data) {
        let decoded = jwt_decode(user.data)
        
        if ((Date.now() / 1000) > decoded.exp) {
            logout(navigation)
        }
    }
    headers['Authorization'] = 'Bearer ' + user.data
    return headers
}

function logout(navigation) {
    localStorage.removeItem("user");
    navigation('/login')
    swal({
        title: 'Oops...',
        msg:'Something bad happened and you have been logged out.', 
        icon:icons.error,
        showConfirmButton:true,
    })
}
