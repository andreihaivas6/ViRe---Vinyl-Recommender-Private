// https://bbbootstrap.com/snippets/bootstrap-5-sidebar-menu-hover-effect-66945518

import '../../assets/styles/sidebar.css'

import { Link } from 'react-router-dom';

import BarButtons from '../bar/buttons/BarButtons';
import LogoutButton from '../bar/buttons/LogoutButton';
import { WIDTH_SIDEBAR } from '../../config/config';

export default function Sidebar() {
    return(
        <div className="d-flex flex-column vh-100 flex-shrink-0 p-3 text-white bg-dark" style={{
            width: WIDTH_SIDEBAR,
            position: "fixed",
            top:0,
        }}>
            <Link to='#' style={{ textDecoration: 'none' }}>
            <div className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none" style={{paddingLeft: 30}}>
                {/* <svg className="bi me-2" width="15" height="1"/> */}
                <div className="fs-4" style={{marginLeft: -3}}>Vinyls</div>
            </div>
            </Link>
        <hr/>
            <ul className="nav nav-pills flex-column mb-auto">
                <BarButtons/>
            </ul>
        <hr/>
            <LogoutButton/>
        </div>
    );
}
