import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import '../assets/styles/friends.css'
import {MDBDataTable} from "mdbreact";
import useFetch from "../helpers/hooks/useFetch";
import {PLAYLIST_PORT, USER_PORT} from "../config/config";
import { useEffect } from "react";
// import { Spinner } from "react-bootstrap";
import Spinner from "../components/Spinner";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";



export default function FriendProfile() {
    const navigate = useNavigate()
    const handleViewPlaylist = (playlist_id) => {
        navigate(`/playlist/${playlist_id}`)
    }

    let { user_id } = useParams();
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    let {fetch_data, data, status, error, isPending} = useFetch(PLAYLIST_PORT, 'playlist/user/' + user_id, 'GET', {immediate: false})
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
            label: 'View Playlist',
            field: 'view', // New column for buttons
            sort: 'disabled',
        },
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
            view: (
                <button className="btn btn-primary" onClick={() => handleViewPlaylist(playlist.playlist_id)}>
                    View Playlist
                </button>
            )
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
                        isPending ? 
                        <Spinner/> : 
                        <div>
                            <h2 className="mx-auto my-0  text-dark pt-5">{data.length > 0 ? data[0].user_name : "Empty"}'s playlists</h2>
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