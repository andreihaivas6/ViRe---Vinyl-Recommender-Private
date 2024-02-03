import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
// import friends style
import '../assets/styles/friends.css'
import {ListGroup, Image, Button, Col, Row} from 'react-bootstrap';
import {MDBDataTable} from "mdbreact";
import useFetch from "../helpers/hooks/useFetch";
import {API_URL, API_URL_USER, USER_PORT} from "../config/config";
import { useEffect } from "react";
// import { Spinner } from "react-bootstrap";
import Spinner from "../components/Spinner";
import { getUserId } from "../helpers/utils";
import { swal, icons,notification } from "../helpers/mySwal";


export default function SearchFriends() {
    const handleAddFriend = (id) => {
        const user = JSON.parse(localStorage.getItem('user'))
        let headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        headers['Authorization'] = 'Bearer ' + user.data
        fetch(API_URL_USER + USER_PORT + 'friendship', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                'user_id': getUserId(),
                'friend_id': id
            })
        }).then(response => {
            console.log(response.status)
            if (response.status === 201) {
                notification('Added friend')
            } else {
                swal({
                    title: 'Already friends',
                    icon: icons.info
                })
            }
        })
    }

    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed
    let {fetch_data, data, status, error, isPending} = useFetch(USER_PORT, 'user', 'GET', {immediate: false})
    useEffect(() => {
        fetch_data()
    }, [])
    
    const columns = [
        {
            label: 'ID',
            field: 'id',
            sort: 'asc',
        },
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
        {
            label: 'Add Friend',
            field: 'actions', // New column for buttons
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
        // let id = user_index + 1
        // user_index to int
        let id_value = parseInt(user_index) + 1
        let id = <div id={id_value}>{id_value}</div>


        rows.push({
            id: id,
            avatar: <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png" alt="Avatar 1" className="friend-profile" />,
            name: user.username,
            full_name: full_name,
            actions: (
                <div>
                    <button className="btn btn-success" onClick={() => handleAddFriend(user.id)}>
                        Add Friend
                    </button>
                </div>
            ),
        })
    }

    const data_to_table = {
        columns,
        rows,
    };

    return (
        <PositionedPage page={
            <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25, padding: 20}}>
                <div className="text-center">
                    {
                        isPending ? <Spinner /> : 
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
        } />
    )
}