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
import { notification } from "../helpers/mySwal";


export default function FriendProfile() {
    const navigate = useNavigate()
    const handleViewPlaylist = (playlist_id) => {
        navigate(`/playlist/${playlist_id}`)
    }

    const handleDeletePlaylist = (playlist_id) => {
        const user = JSON.parse(localStorage.getItem('user'))
        let headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        headers['Authorization'] = 'Bearer ' + user.data
        fetch(`${API_URL_PLAYLIST}${PLAYLIST_PORT}playlist/${playlist_id}`, {
            method: 'DELETE',
            headers: headers,
        })
        .then(response => response.json())
        .then(data => {
            notification('Playlist deleted')
            fetch_data()
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // let { user_id } = useParams();
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    let {fetch_data, data, status, error, isPending} = useFetch(PLAYLIST_PORT, 'playlist', 'GET', {immediate: false})
    useEffect(() => {
        fetch_data()
    }, [])
    
    const columns = [
        {
            label: 'Id',
            field: 'id',
            sort: 'asc', // Disable sorting for the avatar column
        },
        {
            label: 'Playlist',
            field: 'playlist_name',
            sort: 'asc',
        },
        {
            label: 'Description',
            field: 'description',
            sort: 'asc',

        },
        {
            label: 'No tracks',
            field: 'no_tracks', // New column for buttons
            sort: 'asc',
        },
        {
            label: 'Owner',
            field: 'owner', 
            sort: 'asc',
        },
        {
            label: 'View Playlist',
            field: 'view', // New column for buttons
            sort: 'disabled',
        },
        {
            label: 'Delete Playlist',
            field: 'delete', // New column for buttons
            sort: 'disabled',
        }
        ];
    
    let rows = []
    for (let index in data ){
        let playlist = data[index]
        let no_tracks = playlist.tracks !== undefined ? playlist.tracks.length : 0
        rows.push({
            id: parseInt(index) + 1,
            playlist_name: playlist.playlist_name,
            description: playlist.playlist_description,
            no_tracks: no_tracks,
            owner: playlist.user_id == getUserId() ? "Me" : playlist.user_name,
            view: (
                <button className="btn btn-primary" onClick={() => handleViewPlaylist(playlist.playlist_id)}>
                    View Playlist
                </button>
            ),
            delete: (
                <button className="btn btn-danger" onClick={() => handleDeletePlaylist(playlist.playlist_id)}>
                    Delete Playlist
                </button>
            ),
        })
    }

    const handleImportJSPFFile = () => {
        let input = document.getElementById('file');
        let file = input.files[0];
        let reader = new FileReader();
        reader.readAsText(file);
        // print the contents of file
        reader.onload = function(){
                let playlist = JSON.parse(reader.result);
                console.log(playlist)
                const user = JSON.parse(localStorage.getItem('user'))
                let headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
                headers['Authorization'] = 'Bearer ' + user.data

                fetch(`${API_URL_PLAYLIST}${PLAYLIST_PORT}/playlist/import`, {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(playlist),
                })
                .then(response => response.json())
                .then(data => {
                    notification('Playlist imported')
                    // clear the input
                    input.value = ''
                    fetch_data()
                    // refresh the page - but not with fetch_data() - call
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        }
    }

    const handleCreatePlaylist = () => {
        let title = document.getElementById('title').value
        let description = document.getElementById('description').value
        const user = JSON.parse(localStorage.getItem('user'))
        let headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        headers['Authorization'] = 'Bearer ' + user.data
        fetch(`${API_URL_PLAYLIST}${PLAYLIST_PORT}/playlist`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                "playlist_name": title,
                "playlist_description": description
            }),
        })
        .then(response => response.json())
        .then(data => {
            notification('Playlist created')
            fetch_data()
            // clear inputs
            document.getElementById('title').value = ''
            document.getElementById('description').value = ''
        })
        .catch((error) => {
            console.error('Error:', error);
        });
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
                        isPending ? 
                        <Spinner/> : 
                        <div>
                            <h2 className="mx-auto my-0  text-dark pt-5">My playlists</h2>
                            <hr></hr>
                            {/* another 3 items with text input for playlist name, playlist description and a submit button*/}
                            <h3>Create new playlist</h3>
                            <div className="d-flex justify-content-between">
                                <input type="text" id="title" className="form-control m-2" style={{ marginTop: '10px' }} placeholder="Title"/>
                                <input type="text" id="description" className="form-control m-2" style={{ marginTop: '10px' }} placeholder="Description"/>
                                <button className="btn btn-primary m-2" onClick={handleCreatePlaylist}>Create Playlist</button>
                            </div>
                            <hr></hr>
                            <h3>Import JSPF playlist</h3>
                            <div className="d-flex justify-content-between">
                                <input type="file" id="file" accept=".jspf" className="form-control " style={{ marginTop: '10px' }}/>
                                <button className="btn btn-primary" onClick={handleImportJSPFFile}>Import JSPF</button>
                            </div>
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