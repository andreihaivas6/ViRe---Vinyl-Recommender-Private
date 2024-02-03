import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import jwt_decode from "jwt-decode";
import Spinner from "../../components/Spinner";
import useFetch from "../../helpers/hooks/useFetch";
import { swal, icons } from "../../helpers/mySwal";
import {URL_CONFIRMATION_EMAIL, USER_PORT} from "../../config/config";

export default function ConfirmationEmail() {
    const [searchParams] = useSearchParams();

    const navigation = useNavigate()

    const uid = searchParams.get('uid')
    const token = searchParams.get('token')
    const request_url = `${URL_CONFIRMATION_EMAIL}${uid}/${token}/`

    let {data, status} = useFetch(USER_PORT, request_url, 'POST', {})
    
    useEffect(() => {
        if(status === 0) {
            return;
        }

        if (status === 200 || status === 403) {
            if(status === 200) {
                localStorage.setItem("user", JSON.stringify(data.user))
                localStorage.setItem('username', jwt_decode(data.user.access).username)
                navigation('/bots')
            }
            if(status === 403) {
                navigation('/login')
            }

            swal({
                title: (status === 200) ? 'Email successfully verified' : 'Email is already verified',
                icon: icons.success,
            })
        } else {
            navigation(`/resend_confirmation_email?uid=${uid}&token=${token}`)
            swal({
                title: 'Email cannot be verified',
                msg:'Your account is not active yet.',
                icon:icons.error,
                showConfirmButton:true
            })
        }
        
    }, [data])

    return (
        <Spinner/>
    )
}
