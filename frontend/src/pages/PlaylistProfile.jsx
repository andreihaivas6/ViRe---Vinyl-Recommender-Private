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
import { getUserId } from "../helpers/utils";


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
                    
                    {
                        isPending ? 
                        <Spinner/> : 
                        <div>
                            <h2 className="mx-auto my-0  text-dark pt-5">{data.playlist_name}</h2>
                            <h4>{data.playlist_description}</h4>
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