import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import Spinner from "../components/Spinner";
import {spotifyConnect} from "../helpers/spotifyConnect";
import {discogConnect, discogSendVerifier} from "../helpers/discogConnect";
import {useState, useEffect} from "react";
import {useParams,useSearchParams, useLocation } from 'react-router-dom';
import { swal, notification, icons } from "../helpers/mySwal";


export default function Profile() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    const [buttonState, setButtonState] = useState(0);
    const [buttonStateDiscogs, setButtonStateDiscogs] = useState(0);
    const location = useLocation();

    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const oauth_verifier = searchParams.get('oauth_verifier');
        if (oauth_verifier && buttonStateDiscogs === 0) {
            console.log(oauth_verifier);
            discogSendVerifier(oauth_verifier).then(
                res => {
                    console.log(res);
                    setButtonStateDiscogs(1);
                    swal({
                        title: 'You are now connected to Discog!',
                        icon: icons.success
                    })
                }
            )
        }
    }, [location.search]);
    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const code = searchParams.get('code');

        console.log('Code changed:', code);
        if (code && buttonState === 0) {
            spotifyConnect(code);
            setButtonState(1);
            swal({
                title:'You are now connected to Spotify!', 
                icon:icons.success
            })
        }
    }, [location.search]);

    console.log(buttonState, buttonStateDiscogs)

    return (
        <PositionedPage page={
            <div>
                <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25, padding:20}}>
                        <div className="text-center">
                            <h1 className="mx-auto my-0 text-uppercase text-dark pt-5">Profile</h1>
                            <br></br>
                            <h3>Connect your externals apps here</h3>
                            <h2 className="text-dark mx-auto mt-2 mb-5 pt-5">
                                <h3>Sync your Online Playlists from Music Streaming apps</h3>
                                <button 
                                    className={
                                        buttonState === 0 ? "btn btn-primary" : "btn btn-success"
                                    } 
                                    disabled={buttonState !== 0}
                                    onClick={spotifyConnect}>
                                    {buttonState === 0 ? "Sync to Spotify" : "Synced to Spotify!"}

                                </button>
                                
                                <hr></hr>
                                <h3>Sync your Past Purchases from Music Store apps</h3>
                                <button 
                                    className={
                                        buttonStateDiscogs === 0 ? "btn btn-primary" : "btn btn-success"
                                    } 
                                    disabled={buttonStateDiscogs !== 0}
                                    onClick={discogConnect}>
                                    {buttonStateDiscogs === 0 ? "Sync to Discogs" : "Synced to Discogs!"}

                                </button>

                            </h2>
                        </div>
                    </div>
                Discogs
            </div>
        } />
    )
}