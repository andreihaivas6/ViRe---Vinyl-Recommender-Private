import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import img from '../../assets/images/password.jpg'
import {URL_CHOOSE_NEW_PASSWORD, USER_PORT} from '../../config/config';
import useFetch from '../../helpers/hooks/useFetch';
import { icons, swal } from '../../helpers/mySwal';

export default function ResetPassword() {
    const [password, setPassword] = useState("");
    const [passwordCheck, setPasswordCheck] = useState("");
    const [errorName, setErrorName] = useState("");

    const onChangePassword = (e) => {
        setPassword(e.target.value);
    }
    const onChangePasswordCheck = (e) => {
        setPasswordCheck(e.target.value);
    }

    const navigate = useNavigate()

    const [searchParams] = useSearchParams();
    const uid = searchParams.get('uid') 
    const token = searchParams.get('token') 

    let {fetch_data, data, status} = useFetch(USER_PORT, URL_CHOOSE_NEW_PASSWORD, 'POST', {
        immediate: false,
        given_body: {
            'password': password,
            'token': token,
            'uid': uid,
        }
    }) 

    const handleSend = () => {
        if(password === passwordCheck) {
            fetch_data()
        } else {
            setErrorName('Password doesn\'t match with its confirmation.')  
            setPassword('')
            setPasswordCheck('')
        }
    }

    useEffect(() => {
        if(data.length === 0) {
            return;
        }

        if (status === 200) {
            navigate('/login')
            swal({
                title:'Password reset successfully', 
                msg: 'Your password has been reseted. You may log in to your account now.',
                icon:icons.success
            })
        } else {
            if(data.detail) {
                swal({
                    title:'There is a problem', 
                    msg: 'Link has expired. Try to request another one.',
                    icon:icons.error
                })
                navigate('/forgot_password')
            } else {
                setErrorName(data.password[0])
            }
        }
        setPassword('')
        setPasswordCheck('')
    }, [data])


    return (
        <div className="section my_class">
            <div className="container">
                <div className="form">
                    <div className="left-side">
                        <div>
                        <h3 className='p-3' style={{textAlign: "center"}}>Reset Password</h3>

                        <div style={{textAlign: "center", paddingLeft:20, paddingRight:20, paddingTop:5}}>
                            Enter a new password.
                        </div>
                            <div className="form-inputs">
                            <div className="d-flex flex-row align-items-center ">
                                <i className="bi bi-key-fill"></i>
                                <input type="password" placeholder="Password" id='password'
                                value={password} onChange={onChangePassword} style={{marginLeft: 10}}/> 
                            </div>
                            <div className="d-flex flex-row align-items-center ">
                                <i className="bi bi-shield-lock-fill"></i>
                                <input type="password" placeholder="Password check" id='password_check'
                                value={passwordCheck} onChange={onChangePasswordCheck} style={{marginLeft: 10}}/> 
                            </div>

                            <div role="alert" style={{marginBottom: 0, textAlign:'center', color:'red', paddingTop:10}}>
                                {errorName}
                            </div>

                            <div  style={{textAlign: 'center'}}>
                                <input id="submit_button" type="submit" value='Send'
                                    onClick={handleSend} ></input> 
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