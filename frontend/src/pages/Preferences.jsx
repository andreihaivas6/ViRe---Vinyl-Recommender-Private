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

export default function Preferences() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed
    const [preferences, setPreferences] = useState([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const [rows_data, setRowsData] = useState([])
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
    
    const handleSeeVinyl = (vinyl) => {
        // write to localstorage and navigate to vinyl page
        localStorage.setItem('vinyl', JSON.stringify(vinyl))
        navigate('/vinyl/info')
    }

    const handleSentPreference = () => {
        let text = document.getElementById('text').value
        setLoading(true)
        let headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        const user = JSON.parse(localStorage.getItem('user'))
        headers['Authorization'] = 'Bearer ' + user.data
        fetch(API_URL_RECOMMENDATION + RECOMMENDATION_PORT + 'preference', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                "text": text
            })
        })
        .then(response => response.json())
        .then(data => {
            let temp_rows = []
            data.vinyls.forEach((item, index) => {
                temp_rows.push({
                    imageURL: <img src={item.imageUrl} style={{width: 100}}/>,
                    title: item.title,
                    artist: item.artist,
                    genre: item.genre,
                    date: item.date,
                    see_vinyl: (
                        <button className="btn btn-primary" onClick={() => handleSeeVinyl({
                            title: item.title,
                            artist: item.artist,
                            genre: item.genre,
                            date: item.date,
                            imageUrl: item.imageUrl
                        })}>
                            See Vinyl
                        </button>
                    )
                })
            })
            // remove duplicates from temp_rows
            temp_rows = temp_rows.filter((item, index, self) => self.findIndex(t => t.title === item.title) === index)

            setRowsData(temp_rows)
            
            setLoading(false)
        })
    }

    return (
        <PositionedPage page={
            <div className="preferences-container" style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25}}>
                <div className="text-center">
                    {
                        loading ? <Spinner/> :
                        <div className="preferences" style={{width: '70%', margin: 'auto'}}>
                            <h2>Text Preferences</h2>
                            <h5>Enter your input here as examples below:</h5>
                            <div>I always hate rap music</div>
                            <div>I love pop music after 2000</div>
                            <div>I love The Beatles</div>
                            {/* add an input text */}
                            <input type="text" id="text" name="text" placeholder="Enter your text here" style={{width: '100%', padding: 12, margin: 6}}/>
                            <Button variant="primary" style={{margin: 6}} onClick={handleSentPreference}>Submit</Button>
                            <hr/>
                            <h2>Recommendations</h2>
                            <MDBDataTable
                                striped
                                bordered
                                hover
                                data={{columns, rows: rows_data}}
                                noBottomColumns
                                entriesOptions={[5, 10, 20, 50, 100]}
                                entries={5}
                            />
                        </div>
                    }
                    
                </div>
            </div>
        }/>
    )
}