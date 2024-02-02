// https://www.robinwieruch.de/react-router-private-routes/ 

import {Navigate} from 'react-router-dom'
import { swal, icons } from '../mySwal';
import { isLoggedIn } from '../utils';

const PrivateRoute = ({ children }) => {
    if (!isLoggedIn()) {
        swal({
            title:'You are not logged in.',
            icon:icons.error
        })
        return <Navigate to="/login" replace />;
    }
    return children;
};

export default PrivateRoute;
