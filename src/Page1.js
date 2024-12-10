import React from 'react';
import { Link } from 'react-router-dom';

const Page1 = () => {
    return (
        <div>
            <h1>Page 1</h1>
            <p>Welcome to Page 1!</p>
            <Link to="/page2">Go to Page 2</Link>
        </div>
    );
};

export default Page1;
