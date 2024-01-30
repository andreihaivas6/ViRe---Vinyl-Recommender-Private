import { Link } from "react-router-dom"
import { swal, icons } from "../../../helpers/mySwal";

export default function LogoutButton() {
    const handleLogout = () => {
        localStorage.removeItem("user");
        localStorage.removeItem("username");
        
        swal({
            title: 'Successfully logged out.',
            icon: icons.success
        })
    }

    return (
        <Link to='/home' style={{ textDecoration: 'none' }}>
            <div style={{padding: 5}}>
                <div className="nav-link text-white" onClick={handleLogout}> 
                    <i className="bi bi-box-arrow-right"></i>
                    <span className="ms-2">Logout</span> 
                </div> 
            </div>
        </Link>
    )
}