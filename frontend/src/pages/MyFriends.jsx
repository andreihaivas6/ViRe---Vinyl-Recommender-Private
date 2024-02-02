import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import '../assets/styles/friends.css'
import {MDBDataTable} from "mdbreact";
import {spotifyConnect} from "../helpers/spotifyConnect";


function handleViewProfile(index) {
}

function handleRemoveFriend(index) {
}

export default function Friends() {

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
            label: 'Remove Friend',
            field: 'remove', // New column for buttons
            sort: 'disabled',
        },
        {
            label: 'View Profile',
            field: 'view', // New column for buttons
            sort: 'disabled',
        },
        ];

    const rows = [
        {
            avatar: <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png" alt="Avatar 1" className="friend-profile" />,
            name: 'John Doe',
            age: 25,
            remove: (
                    <button className="btn btn-danger" onClick={() => handleRemoveFriend()}>
                        Remove Friend
                    </button>),
            view: (
                    <button className="btn btn-primary" onClick={() => handleViewProfile()}>
                        View Profile
                    </button>
            ),
        },
        {
            avatar: <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png" alt="Avatar 2" className="friend-profile"/>,
            name: 'Jane Doe',
            age: 30,
            remove: (
                <button className="btn btn-danger" onClick={() => handleRemoveFriend()}>
                    Remove Friend
                </button>),
            view: (
                <button className="btn btn-primary" onClick={() => handleViewProfile()}>
                    View Profile
                </button>
            ),
        },
    ];
    const data = {
        columns,
        rows,
    };
                
    return (
        <PositionedPage page={
            <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius: 25}}>
                <div className="text-center">
                    <MDBDataTable
                        striped
                        bordered
                        hover
                        data={data}
                    />

                </div>
                    <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25}}>
                        <div className="text-center">
                            <h1 className="mx-auto my-0 text-uppercase text-dark pt-5">Demo</h1>
                            <h2 className="text-dark mx-auto mt-2 mb-5 pt-5">
                                This is a demo page.
                                <h1>Display your Spotify profile data</h1>
                                <button onClick={spotifyConnect}>
                                    Click me
                                </button>

                            </h2>
                        </div>
                    </div>
            </div>
        }/>
    )
}