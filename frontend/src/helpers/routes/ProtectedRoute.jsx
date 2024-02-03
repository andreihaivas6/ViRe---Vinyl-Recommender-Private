import {Navigate} from 'react-router-dom'
import { swal, icons } from '../mySwal';
import { isLoggedIn } from '../utils';

const ProtectedRoute = ({ children }) => {
    if (isLoggedIn()) {
        swal({
            title:'You are logged in.', 
            icon:icons.info
        })
        return <Navigate to="/preferences" replace />;
    }
    return children;
};

export default ProtectedRoute;
