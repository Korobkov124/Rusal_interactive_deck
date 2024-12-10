import React from 'react';
import { Link } from 'react-router-dom';
import './main.css';
const Page1 = () => {
    return (
        <div id='root1'>
        <div id="left_header">
                <button type="button" className="header_buttons"><img src="/pngs/Generic avatar.svg"></img></button>
                <button type="button" className="header_buttons"><img src="/pngs/today.svg"></img></button>
                <button type="button" className="header_buttons"><img src="/pngs/add.svg"></img></button>
            </div>
                <div id="right_header">
                <img src="/pngs/logo.png" alt="" width="107px" height="107px"></img>
            </div>
        </div>
    );
};

export default Page1;
