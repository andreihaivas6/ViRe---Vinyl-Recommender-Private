import '../../assets/styles/home.css'

import { useEffect, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom";

import RightImg from '../../assets/images/email.png'
import useFetch from "../../helpers/hooks/useFetch";
import { icons, swal } from "../../helpers/mySwal";
import { URL_RESEND_CONFIRMATION_EMAIL, USER_PORT } from "../../config/config";

export default function ResendConfirmationEmail() {
    const [email, setEmail] = useState("");
    const [errorName, setErrorName] = useState("");

    const onChangeEmail = (e) => {
        setEmail(e.target.value);
    }

    const [searchParams] = useSearchParams();
    const navigation = useNavigate()

    const uid = searchParams.get('uid')    
    const token = searchParams.get('token') 
    const url = `${URL_RESEND_CONFIRMATION_EMAIL}${uid}/${token}/${email}/`

    let {fetch_data, data, status} = useFetch(USER_PORT, url, 'POST', {
        immediate: false
    }) 

    const handleResend = () => {
        fetch_data()
    }

    useEffect(() => {
        if(data.length === 0) {
            return;
        }

        if (status === 200) {
            navigation('/login')
            swal({
                title:data.message, 
                icon:icons.success
            })
        } else {
            setErrorName(data.message)
        }
    }, [data])
    
    return (
        <div className="section my_class">
            <div className="container">
                <div className="form">
                    <div className="left-side">
                        <div>
                        <h3 className='p-3' style={{textAlign: "center"}}>Activation Email</h3>

                        <div style={{textAlign: "center", paddingLeft:20, paddingRight:20, paddingTop:5}}>Enter your email in order to send another confirmation link.</div>
                        
                            <div className="form-inputs">
                            <div className="d-flex flex-row align-items-center ">
                                <i className="bi bi-envelope-fill"></i>
                                <input type="text" placeholder="Email Address" id='email'
                                value={email} onChange={onChangeEmail} style={{marginLeft: 10}}/> 
                            </div>

                            <div role="alert" style={{marginBottom: 0, textAlign:'center', color:'red', paddingTop:10}}>
                                {errorName}
                            </div>


                            <div style={{textAlign: 'center'}}>
                                <input id="submit_button" type="submit" value='Resend' onClick={handleResend}></input> 
                            </div>
                                
                            </div>
                        </div>
                    </div>

                    <div className="right-side">
                        <img src={RightImg} width="auto" height="100%" alt=""/>
                    </div>
                    
                </div>
            </div>
        </div>
    )
}
