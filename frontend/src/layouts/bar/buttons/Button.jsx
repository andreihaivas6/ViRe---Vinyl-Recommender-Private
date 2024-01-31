import { NavLink } from "react-router-dom"

export default function Button({link_to, icon, text_button}) {
    return (
        <div style={{padding: 5}}>
            <NavLink 
                to={link_to} 
                style={{ textDecoration: 'none'}} 
                className = "nav-link text-white" 
                activeclassname="nav-link active" 
            >
            <div>
                <div> 
                    {icon}
                    <span className="ms-2">{text_button}</span> 
                </div>
            </div>
            </NavLink>
        </div>
    )
}