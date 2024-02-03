import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import '../assets/styles/friends.css'
import {MDBDataTable} from "mdbreact";
import useFetch from "../helpers/hooks/useFetch";
import {USER_PORT} from "../config/config";
import { useEffect } from "react";
// import { Spinner } from "react-bootstrap";
import Spinner from "../components/Spinner";
import { useNavigate } from "react-router-dom";



export default function Friends() {
    const navigate = useNavigate()

    const handleViewProfile = (user_id) => {
        navigate(`/profile/${user_id}`)
    }

    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    // useFetch to get friends
    let {fetch_data, data, status, error, isPending} = useFetch(USER_PORT, 'friends', 'GET', {immediate: false})
    useEffect(() => {
        fetch_data()
    }, [])
    
    const columns = [
        {
            label: 'Avatar',
            field: 'avatar',
            sort: 'disabled', // Disable sorting for the avatar column
        },
        {
            label: 'Username',
            field: 'name',
            sort: 'asc',
        },
        {
            label: 'Full name',
            field: 'full_name',
            sort: 'asc',

        },
        // {
        //     label: 'Remove Friend',
        //     field: 'remove', // New column for buttons
        //     sort: 'disabled',
        // },
        {
            label: 'View Profile',
            field: 'view', // New column for buttons
            sort: 'disabled',
        },
        ];
    
    let rows = []
    for (let user_index in data ){
        let user = data[user_index]
        let full_name = (user.first_name != null ? user.first_name : "") + 
            " " + 
            (user.last_name != null ? user.last_name : "")
        if (full_name === " "){
            full_name = "N/A"
        }

        rows.push({
            avatar: <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png" alt="Avatar 1" className="friend-profile" />,
            name: user.username,
            full_name: full_name,
            // remove: (
            //     <button className="btn btn-danger" onClick={() => handleRemoveFriend()}>
            //         Remove Friend
            //     </button>),
            view: (
                <button className="btn btn-primary" onClick={() => handleViewProfile(user.id)}>
                    View Profile
                </button>
            ),
        })
    }

    const data_to_table = {
        columns,
        rows,
    };
 
    return (
        <PositionedPage page={
            <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius: 25, padding: 20}}>
                <div className="text-center">
                    {
                        isPending ? 
                        <Spinner/> : 
                        <MDBDataTable
                            striped
                            bordered
                            hover
                            data={data_to_table}
                            noBottomColumns
                            entriesOptions={[5, 10, 20, 50, 100]}
                            entries={5}
                        />
                    }
                </div>
                    
            </div>
        }/>
    )
}