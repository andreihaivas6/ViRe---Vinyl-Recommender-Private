import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import '../assets/styles/preferences.css';
import {Button, Form} from "react-bootstrap";
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

export default function Preferences() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed
    const [preferences, setPreferences] = useState([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    


    const handleSentPreference = () => {
        let text = document.getElementById('text').value
        setLoading(true)
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
                        </div>
                    }
                    
                </div>
            </div>
        }/>
    )
}