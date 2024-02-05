import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import '../assets/styles/preferences.css';
import {Button, Form} from "react-bootstrap";

import {MDBDataTable} from "mdbreact";
import useFetch from "../helpers/hooks/useFetch";
import {API_URL_PLAYLIST, API_URL_RECOMMENDATION, PLAYLIST_PORT, RECOMMENDATION_PORT, USER_PORT} from "../config/config";
import { useEffect } from "react";
// import { Spinner } from "react-bootstrap";
import Spinner from "../components/Spinner";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import { getUserId } from "../helpers/utils";
import { useState } from "react";
import { notification, swal, icons } from "../helpers/mySwal";


export default function Recommendations() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed
    // const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    let {fetch_data, data, isPending} = useFetch(RECOMMENDATION_PORT, 'recommend', 'GET', {immediate: true})
    // useEffect(() => {
    //     fetch_data()
    // }, [])

    const [rows_data_complete, setRowsDataComplete] = useState([])
    const [rows_data_by_artist, setRowsDataByArtist] = useState([])
    const [rows_data_by_genre, setRowsDataByGenre] = useState([])

    const columns = [
        {
            label: 'Image',
            field: 'imageURL',
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
            label: 'Genre',
            field: 'genre', // New column for buttons
            sort: 'asc',
        },
        {
            label: 'Date',
            field: 'date', 
            sort: 'asc',
        },
        {
            label: "See Vinyl",
            field: "see_vinyl", // button
            sort: "disabled",
        }
        
    ];

    useEffect(() => {

        if (data !== undefined && data.data !== undefined) { 
            console.log(data)
            let rows_complete = []
            let rows_by_artist = []
            let rows_by_genre = []

            for (let index in data.data.complete.vinyls) {
                let vinyl = data.data.complete.vinyls[index]
                console.log(vinyl)
                rows_complete.push({
                    imageURL: <img src={vinyl.imageUrl} style={{width: 50, height: 50}}/>,
                    title: vinyl.title,
                    artist: vinyl.artist,
                    genre: vinyl.genre,
                    date: vinyl.date,
                    see_vinyl: <Button onClick={() => handleSeeVinyl(vinyl)}>See Vinyl</Button>
                })
            }
            rows_complete = rows_complete.filter((item, index, self) => self.findIndex(t => t.title === item.title) === index)

            for (let index in data.data.by_artist.vinyls) {
                let vinyl = data.data.by_artist.vinyls[index]
                let row = {
                    imageURL: <img src={vinyl.imageUrl} style={{width: 50, height: 50}}/>,
                    title: vinyl.title,
                    artist: vinyl.artist,
                    genre: vinyl.genre,
                    date: vinyl.date,
                    see_vinyl: <Button onClick={() => handleSeeVinyl(vinyl)}>See Vinyl</Button>
                }
                rows_by_artist.push(row)
            }
            rows_by_artist = rows_by_artist.filter((item, index, self) => self.findIndex(t => t.title === item.title) === index)
            

            for (let index in data.data.by_genre.vinyls) {
                let vinyl = data.data.by_genre.vinyls[index]
                let row = {
                    imageURL: <img src={vinyl.imageUrl} style={{width: 50, height: 50}}/>,
                    title: vinyl.title,
                    artist: vinyl.artist,
                    genre: vinyl.genre,
                    date: vinyl.date,
                    see_vinyl: <Button onClick={() => handleSeeVinyl(vinyl)}>See Vinyl</Button>
                }
                rows_by_genre.push(row)
            }
            rows_by_genre = rows_by_genre.filter((item, index, self) => self.findIndex(t => t.title === item.title) === index)
            
            setRowsDataComplete(rows_complete)
            setRowsDataByArtist(rows_by_artist)
            setRowsDataByGenre(rows_by_genre)
        }
    }, [isPending])
    
    const handleSeeVinyl = (vinyl) => {
        // write to localstorage and navigate to vinyl page
        localStorage.setItem('vinyl', JSON.stringify(vinyl))
        navigate('/vinyl/info')
    }

    return (
        <PositionedPage page={
            <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25, padding: 20}}>
                <div className="text-center">
                    
                    {
                        isPending ?
                        <Spinner/> :
                        <div>
                            <h1 className="mx-auto my-0  text-dark pt-5">Recommendations</h1>
                            <h2 className="mx-auto my-0  text-dark pt-5">General recommendation</h2>
                            <MDBDataTable
                                striped
                                bordered
                                // small
                                data={{
                                    columns,
                                    rows: rows_data_complete
                                }}
                                entriesOptions={[5, 10, 20, 50, 100]}
                                entries={5}
                            />
                            <h2 className="mx-auto my-0  text-dark pt-5">Recommendation based on your favorite artists</h2>
                            <MDBDataTable
                                striped
                                bordered
                                // small
                                data={{
                                    columns,
                                    rows: rows_data_by_artist
                                }}
                                entriesOptions={[5, 10, 20, 50, 100]}
                                entries={5}
                            />
                            <h2 className="mx-auto my-0  text-dark pt-5">Recommendations based on your favorite genres</h2>
                            <MDBDataTable
                                striped
                                bordered
                                // small
                                data={{
                                    columns,
                                    rows: rows_data_by_genre
                                }}
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