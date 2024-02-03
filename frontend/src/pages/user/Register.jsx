// https://bbbootstrap.com/snippets/animated-login-form-password-hide-show-and-password-suggestion-59879684

import '../../assets/styles/login.css'
import '../../assets/styles/home.css'

import RightImg from '../../assets/images/bg.jpg'

import { Link, useNavigate } from "react-router-dom"
import { useState, useEffect } from 'react';

import useFetch from '../../helpers/hooks/useFetch';
import { swal, icons } from '../../helpers/mySwal';
import {URL_REGISTER, USER_PORT} from '../../config/config';


export default function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [passwordCheck, setPasswordCheck] = useState("");
    const [errorName, setErrorName] = useState("");

    const navigation = useNavigate();

    const onChangeUsername = (e) => {
        setUsername(e.target.value);
    }
    const onChangeEmail = (e) => {
        setEmail(e.target.value);
    }
    const onChangePassword = (e) => {
        setPassword(e.target.value);
    }
    const onChangePasswordCheck = (e) => {
        setPasswordCheck(e.target.value);
    }


    let {fetch_data, data, status} = useFetch(USER_PORT, URL_REGISTER, 'POST',
        {
        given_body:{
        'username': username,
        'email': email,
        'password_hash': password,
        },
        needs_auth: false,
        immediate: false})

    const handleRegister = () => {
        fetch_data()
    }

    useEffect(() => {
        if (data.length === 0) {
            return;
        }

        if (status === 201) {
            navigation('/login')
            swal({
                title:'Account successfully created.', 
                msg:'A confirmation link will be sent to your email address shortly...',
                icon:icons.success,
                showConfirmButton:true
            })
        } 
        else {
            let msg = 'error'
            for (const property in data) {
                msg = `${property}: ${data[property][0]}`
                break
            }

            setErrorName(msg)
            setPassword('')
            setPasswordCheck('')
        }
    }, [data])


    return (
        <div className="section my_class">
            <div className="container">
                <div className="form">
                    <div className="left-side">
                        <div>    
                            <div className="form-inputs">

                            <h3 style={{textAlign: "center"}}>Register</h3>

                            <div className="d-flex flex-row align-items-center ">
                                <i className="bi bi-person-fill"></i>
                                <input type="text" placeholder="Username" id='username'
                                value={username} onChange={onChangeUsername} style={{marginLeft: 10}}/> 
                            </div>
                            <div className="d-flex flex-row align-items-center ">
                                <i className="bi bi-envelope-fill"></i>
                                <input type="text" placeholder="Email Address" id='email'
                                value={email} onChange={onChangeEmail} style={{marginLeft: 10}}/> 
                            </div>
                            <div className="d-flex flex-row align-items-center  password">
                                <i className="bi bi-key-fill"></i>
                                <input id="password" type="password" placeholder="Password" 
                                value={password} onChange={onChangePassword} style={{marginLeft: 10}}/> 
                            </div>
                            <div className="d-flex flex-row align-items-center  password">
                                <i className="bi bi-shield-lock-fill"></i>
                                <input id="password_check" type="password" placeholder="Password check" 
                                value={passwordCheck} onChange={onChangePasswordCheck} style={{marginLeft: 10}}/> 
                            </div>

                            <div role="alert" style={{marginBottom: 0, textAlign:'center', color:'red', paddingTop:10}}>
                                {errorName}
                            </div>
                                
                                <div style={{textAlign: 'center'}}>
                                    <input id="submit_button" type="submit" value='Sign Up' onClick={handleRegister}></input> 
                                </div>
                                <div className="login-text" >Already have an account?
                                    <Link to={'/login'} >
                                        <div >Login</div>
                                    </Link>
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
