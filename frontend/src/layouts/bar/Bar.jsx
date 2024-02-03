import useWindowDimension from "../../helpers/hooks/useWindowDimension";
import NavbarResponsive from "../navbar/NavbarResponsive";
import Sidebar from "../sidebar/Sidebar";
import ProfileButton from "./buttons/ProfileButton";

import { WIDTH_FOR_RESPONSIVENESS } from "../../config/config";

export default function Bar() {
    const dimension = useWindowDimension();
    
    if(dimension.width <= WIDTH_FOR_RESPONSIVENESS) {
        return (
            <NavbarResponsive style={{position: "fixed"}}/>
        )
    }
    else {
        return (
            <div className = "myBar">
                <nav className="navbar navbar-expand-lg navbar-light bg-dark text-white" style={{width: dimension.width - 20}}>
                    <div className="container-fluid">
                        <svg className="bi me-2" width="40" height="32"/>
                        <span className="fs-4"></span> 

                        <div style={{display: "flex"}}>
                            {/* <div className="nav-link text-white" style={{margin: 5}}>
                                <i className="bi bi-bell" ></i>
                            </div> */}
                            <ProfileButton/>
                        </div>

                    </div>
                </nav>
                
                <Sidebar/>
                
            </div>
        )
    }
}