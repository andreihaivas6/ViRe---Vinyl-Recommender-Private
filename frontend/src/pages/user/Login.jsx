// https://bbbootstrap.com/snippets/animated-login-form-password-hide-show-and-password-suggestion-59879684

import '../../assets/styles/login.css'
import '../../assets/styles/home.css'
import RightImg from '../../assets/images/bg-1.jpg'
import { useNavigate } from "react-router-dom";

import { Link } from "react-router-dom"
import { useEffect, useState } from 'react';

import useFetch from '../../helpers/hooks/useFetch';
import {URL_LOGIN, USER_PORT} from '../../config/config';
import { swal, icons } from '../../helpers/mySwal';
import jwt_decode from "jwt-decode";


export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorName, setErrorName] = useState("");
    const [sent, setSent] = useState(false)

    const navigation = useNavigate()

    const onChangeUsername = (e) => {
        setUsername(e.target.value);
    }
    const onChangePassword = (e) => {
        setPassword(e.target.value);
    }
    
    let {fetch_data, data, status} = useFetch(USER_PORT, URL_LOGIN, 'POST', {
        given_body:{
            'username': username,
            'password_hash': password
        }, 
        immediate: false,
        needs_auth: false
    }) 

    const handleLogin = () => {
        console.log('login pressed')
        fetch_data()
    }

    useEffect(() => {
        if (data.length === 0) {
            return;
        }

        if(status === 200) {
            swal({
                title:'Credentials are correct', 
                msg: 'A confirmation link has been sent to your email in order to end your login.',
                showConfirmButton: true,
                icon:icons.success
            })
            setUsername('')
            setPassword('')

            localStorage.setItem("user", JSON.stringify(data))
            navigation('/preferences')
            swal({
                title:'Successfully logged in.',
                icon:icons.success
            })
            localStorage.setItem('username', jwt_decode(data.data).username)

            setSent(true)
        } 
        else {
            let msg = 'error'
            if (data.username && data.password) {
                msg = 'Username/Password: ' + data.username
            } else if (data.username) {
                msg = 'Username: ' + data.username
            } else if (data.password) {
                msg = 'Password: ' + data.password
            } else if (data.detail){
                msg = data.detail
            }
            
            setErrorName(msg)
            setPassword('')
            console.log(data)
        }
    }, [data])

    return (
        <div className="section my_class" >
            <div className="container" >
                <div className="form" >
                    <div className="left-side" >
                        <div>
                        <h3 style={{textAlign: "center"}}>Login</h3>
                        
                            <div className="form-inputs">
                            <div className="d-flex flex-row align-items-center ">
                                <i className="bi bi-person-fill"></i>
                                <input type="text" placeholder="Username" id='username'
                                value={username} onChange={onChangeUsername} style={{marginLeft: 10}}/> 
                            </div>
                            <div className="d-flex flex-row align-items-center  password" >
                                <i className="bi bi-key-fill"></i>
                                <input id="password" type="password" placeholder="Password" 
                                value={password} onChange={onChangePassword} style={{marginLeft: 10}}/> 
                            </div>

                            <div role="alert" style={{marginBottom: 0, textAlign:'center', color:'red', paddingTop:10}}>
                                {errorName}
                            </div>

                                <div style={{textAlign: 'center'}}>
                                    <input id="submit_button" type="submit" value='Log In' 
                                    onClick={handleLogin} disabled={sent}></input> 
                                </div>
                                <div className="login-text" >Don't have an account?
                                    <Link to={'/register'} >
                                        <div>Register</div>
                                    </Link>
                                </div>

                                <div className="login-text" >Forgot your password?
                                    <Link to={'/forgot_password'} >
                                        <div>Recover it</div>
                                    </Link>
                                </div>

                            </div>
                        </div>
                    </div>
                    <div className="right-side">
                        <img src={RightImg} style={{ filter: 'grayscale(100%)', width: 'auto', height: '100%' }} alt="" />
                    </div>
                </div>
            </div>
        </div>
    )
}