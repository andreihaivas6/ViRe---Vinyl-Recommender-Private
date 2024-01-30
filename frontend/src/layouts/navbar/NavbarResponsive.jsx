// https://getbootstrap.com/docs/5.1/components/navbar/

import BarButtons from "../bar/buttons/BarButtons"
import LogoutButton from "../bar/buttons/LogoutButton"
import ProfileButton from "../bar/buttons/ProfileButton"
import {Button} from "react-bootstrap";

export default function NavbarResponsive() {
    return (
        <nav className="myBar navbar navbar-expand-lg navbar-light bg-dark text-white" >
            <div className="container-fluid" style={{margin: 5}}>
                <div>
                    <span className="fs-4" style={{paddingLeft: 20}}>Vinyl</span>
                </div>

                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon" ></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarNavDropdown" >
                <ul className="nav nav-pills flex-column mb-auto">
                    <hr/>
                    <ProfileButton/>
                    <BarButtons/>
                    <LogoutButton/>
                </ul>
                </div>
            </div>
        </nav>
    )
}
