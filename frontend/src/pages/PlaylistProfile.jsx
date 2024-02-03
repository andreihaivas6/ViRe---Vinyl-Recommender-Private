import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import '../assets/styles/friends.css'
import {MDBDataTable} from "mdbreact";
import useFetch from "../helpers/hooks/useFetch";
import {API_URL_PLAYLIST, PLAYLIST_PORT, USER_PORT} from "../config/config";
import { useEffect } from "react";
// import { Spinner } from "react-bootstrap";
import Spinner from "../components/Spinner";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import { getUserId } from "../helpers/utils";
import { useState } from "react";
import { notification, swal, icons } from "../helpers/mySwal";


export default function PlaylistProfile() {
    const navigate = useNavigate()
    // const handleViewPlaylist = (playlist_id) => {
    //     navigate(`/playlist/${playlist_id}`)
    // }

    let { playlist_id } = useParams();
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    let {fetch_data, data, status, error, isPending} = useFetch(PLAYLIST_PORT, 'playlist/' + playlist_id , 'GET', {immediate: false})
    useEffect(() => {
        fetch_data()
    }, [])

    let fetch_friends = useFetch(USER_PORT, 'friends', 'GET', {immediate: true})

    const [username, setUsername] = useState('')

    let fetch_share_playlist = useFetch(PLAYLIST_PORT, 'playlist/share', 'POST', {
        immediate: false,
        given_body: {
            "playlist_id": playlist_id,
            "shared_with_user_name": username
        }
    })

    const columns = [
        {
            label: 'Id',
            field: 'id',
            sort: 'asc', // Disable sorting for the avatar column
        },
        {
            label: 'Title',
            field: 'title',
            sort: 'asc',
        },
        {
            label: 'Artist',
            field: 'artist',
            sort: 'asc',

        },
        {
            label: 'Album',
            field: 'album', // New column for buttons
            sort: 'asc',
        },
        {
            label: 'Duration',
            field: 'duration', 
            sort: 'asc',
        },
        {
            label: 'Genre',
            field: 'genre', // New column for buttons
            sort: 'asc',
        },
        {
            label: 'Data',
            field: 'date', // New column for buttons
            sort: 'asc',
        }
    ];
    
    let rows = []
    for (let index in data.tracks ){
        let playlist = data.tracks[index]
        rows.push({
            id: parseInt(index) + 1,
            title: playlist.title,
            artist: playlist.artist,
            album: playlist.album,
            duration: playlist.duration,
            genre: playlist.genre,
            date: playlist.date,
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
                {/* a flex with 2 components: Share with *dropdown* with usernames from fetch_friends and a button with a request */}
                
                    
                    {
                        isPending ? 
                        <Spinner/> : 
                        data.user_id == getUserId() ?
                            <div>
                                <h2 className="mx-auto my-0  text-dark pt-5">{data.playlist_name}</h2>
                                <h4>{data.playlist_description}</h4>
                                <hr></hr>
                                    <MDBDataTable
                                        striped
                                        bordered
                                        hover
                                        data={data_to_table}
                                        noBottomColumns
                                        entriesOptions={[5, 10, 20, 50, 100]}
                                        entries={5}
                                    />
                            <div className="d-flex justify-content-between">
                                <div className="m-3">
                                    Share with:
                                    </div>
                                <select className="m-3 form-select" aria-label="Default select example" id="share_with">
                                    <option value="0">Select a friend</option>
                                    {fetch_friends.data.map((friend) => {
                                        return <option value={friend.username}>{friend.username}</option>
                                    })}
                                </select>
                                <button className="m-3 btn btn-primary" onClick={() => {
                                    // setUsername(document.getElementById('share_with').value)
                                    const user = JSON.parse(localStorage.getItem('user'))
                                    let headers = {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json',
                                    }
                                    headers['Authorization'] = 'Bearer ' + user.data
                                    fetch(API_URL_PLAYLIST + PLAYLIST_PORT + 'playlist/share', {
                                        method: 'POST',
                                        headers: headers,
                                        body: JSON.stringify({
                                            "playlist_id": playlist_id,
                                            "shared_with_user_name": document.getElementById('share_with').value
                                        })
                                    }).then(response => {
                                        console.log(response.status)
                                        if (response.status === 201) {
                                            notification('Shared playlist')
                                        } else {
                                            swal({
                                                title: 'Already shared',
                                                icon: icons.info
                                            })
                                        }
                                    })
                                }}>Share playlist</button>
                                </div>
                            </div>
                             : 
                            <div>
                                <h2 className="mx-auto my-0  text-dark pt-5">{data.playlist_name}</h2>
                                <h4>{data.playlist_description}</h4>
                                <hr></hr>
                                <MDBDataTable
                                    striped
                                    bordered
                                    hover
                                    data={data_to_table}
                                    noBottomColumns
                                    entriesOptions={[5, 10, 20, 50, 100]}
                                    entries={5}
                                />
                            </div>
                    }
                </div>
            </div>
        } />
    )
}