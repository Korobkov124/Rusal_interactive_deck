import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './auth.css';
const AuthPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSignIn = () => {
        const validEmail = 'user@example.com';
        const validPassword = 'password123';

        if (email === validEmail && password === validPassword) {
            navigate('/page1');
        } else {
            alert('Неверный логин или пароль');
        }
    };
    return (
        <div>
            <div id="right_header">
                <img src="/pngs/logo.png" alt="" width="107px" height="107px" />
            </div>
            <div id="auth_form">
                <h1>Coworking booking</h1>
                <p>Login</p>
                <input 
                    type="text" 
                    id="Email_input" 
                    className="auth_input" 
                    placeholder="Login" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)} 
                />
                <p>Password</p>
                <input 
                    type="password" 
                    id="Password_input" 
                    className="auth_input" 
                    placeholder="Password" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)} 
                />
                <button id="auth_button_sign_in" onClick={handleSignIn}>Sign in</button>
                <button id="auth_button_sign_out">Sign up</button>
            </div>
        </div>
    );
};
export default AuthPage;
