import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import jwt_decode from "jwt-decode";

import Spinner from "../../components/Spinner";
import useFetch from "../../helpers/hooks/useFetch";
import { swal, icons } from "../../helpers/mySwal";
import {URL_LOGIN_EMAIL, USER_PORT} from "../../config/config";

export default function ConfirmationLogin() {
    const [searchParams] = useSearchParams();

    const navigation = useNavigate()

    const uid = searchParams.get('uid')
    const token = searchParams.get('token')
    const request_url = `${URL_LOGIN_EMAIL}${uid}/${token}/`

    let {data, status} = useFetch(USER_PORT, request_url, 'POST', {})

    useEffect(() => {
        if(status === 0) {
            return;
        }

        if (status === 200) {
            localStorage.setItem("user", JSON.stringify(data))
            navigation('/bots')
            swal({
                title:'Successfully logged in.', 
                icon:icons.success
            })
            localStorage.setItem('username', jwt_decode(data.access).username)

        } else {
            swal({
                title: 'Unsuccessful login attempt',
                msg:'Link has expired. Try to login again.',
                icon:icons.error,
                showConfirmButton:true
            })
            navigation('/login')
        }
        
    }, [data])

    return (
        <div>
            <Spinner/>  
        </div>
    )
}
