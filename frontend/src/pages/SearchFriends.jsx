import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
// import friends style
import '../assets/styles/friends.css'
import {ListGroup, Image, Button, Col, Row} from 'react-bootstrap';
import {MDBDataTable} from "mdbreact";


function handleAddFriend(index) {

}

export default function SearchFriends() {

    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed
    const users = [
        { id: 1, firstName: 'John', lastName: 'Doe', avatarUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png' },
        { id: 2, firstName: 'Jane', lastName: 'Smith', avatarUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png' },
        { id: 3, firstName: 'John', lastName: 'Smith', avatarUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png' },
    ];
    const columns = [
        {
            label: 'Avatar',
            field: 'avatar',
            sort: 'disabled', // Disable sorting for the avatar column
        },
        {
            label: 'Name',
            field: 'name',
            sort: 'asc',
        },
        {
            label: 'Age',
            field: 'age',
            sort: 'asc',

        },
        {
            label: 'Actions',
            field: 'actions', // New column for buttons
            sort: 'disabled',
        },
    ];

    const rows = [
        {
            avatar: <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png" alt="Avatar 1" className="friend-profile" />,
            name: 'John Doe',
            age: 25,
            actions: (
                <div>
                    <button className="btn btn-success" onClick={() => handleAddFriend()}>
                        Add Friend
                    </button>
                </div>
            ),
        },
        {
            avatar: <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png" alt="Avatar 2" className="friend-profile"/>,
            name: 'Jane Doe',
            age: 30,
            actions: (
                <div>
                    <button className="btn btn-success" onClick={() => handleAddFriend()}>
                        Add Friend
                    </button>
                </div>
            ),
        },
    ];
    const data = {
        columns,
        rows,
    };

    return (
        <PositionedPage page={
            <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25}}>
                <div className="text-center">
                    <MDBDataTable
                        striped
                        bordered
                        hover
                        data={data}
                    />

                </div>
            </div>
        } />
    )
}