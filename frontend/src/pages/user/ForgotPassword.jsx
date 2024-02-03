import { useEffect, useState } from 'react';
import img from '../../assets/images/password_forgot.jpg'
import {URL_FORGOT_PASSWORD, USER_PORT} from '../../config/config';
import useFetch from '../../helpers/hooks/useFetch';
import { icons, swal } from '../../helpers/mySwal';


export default function ForgotPassword() {
    const [email, setEmail] = useState("");
    const [errorName, setErrorName] = useState("");
    const [sent, setSent] = useState(false)

    const onChangeEmail = (e) => {
        setEmail(e.target.value);
    }

    let {fetch_data, data, status} = useFetch(USER_PORT, URL_FORGOT_PASSWORD, 'POST', {
        immediate: false,
        given_body: {
            'email': email
        }
    }) 

    const handleSend = () => {
        fetch_data()   
    }

    useEffect(() => {
        if(data.length === 0) {
            return;
        }

        if (status === 200) {
            swal({
                title:'Email is correct', 
                msg: 'A confirmation link has been sent to your email in order to reset your password.',
                showConfirmButton: true,
                icon:icons.success
            })
            setErrorName('Check your email adrress.')
            setSent(true)
        } else {
            setErrorName(data.email)
        }
        setEmail('')
    }, [data])


    return (
        <div className="section my_class">
            <div className="container">
                <div className="form">
                    <div className="left-side">
                        <div>
                        <h3 className='p-3' style={{textAlign: "center"}}>Forgot Password</h3>

                        <div style={{textAlign: "center", paddingLeft:20, paddingRight:20, paddingTop:5}}>
                            Enter your email in order to send a link to reset your password.
                        </div>
                            <div className="form-inputs">
                            <div className="d-flex flex-row align-items-center ">
                                <i className="bi bi-envelope-fill"></i>
                                <input type="text" placeholder="Email Address" id='email'
                                value={email} onChange={onChangeEmail} style={{marginLeft: 10}}/> 
                            </div>

                            <div role="alert" style={{marginBottom: 0, textAlign:'center', color:'red', paddingTop:10}}>
                                {errorName}
                            </div>

                            <div  style={{textAlign: 'center'}}>
                                <input id="submit_button" type="submit" value='Send'
                                    onClick={handleSend} disabled={sent}></input> 
                            </div>
                                
                            </div>
                        </div>
                    </div>

                    <div className="right-side">
                        <img src={img} width="auto" height="100%" alt=""/>
                    </div>
                    
                </div>
            </div>
        </div>
    )
}