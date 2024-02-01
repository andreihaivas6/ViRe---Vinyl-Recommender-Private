import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import Spinner from "../components/Spinner";
import "../helpers/spotifyConnect" ;

export default function Demo() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    return (
        <PositionedPage page={
            <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25}}>
                <div className="text-center">
                    <h1 className="mx-auto my-0 text-uppercase text-dark pt-5">Demo</h1>
                    <h2 className="text-dark mx-auto mt-2 mb-5 pt-5">
                        This is a demo page.
                        <h1>Display your Spotify profile data</h1>

                        <section id="profile">
                            <h2>Logged in as <span id="displayName"></span></h2>
                            <span id="avatar"></span>
                            <ul>
                                <li>User ID: <span id="id"></span></li>
                                <li>Email: <span id="email"></span></li>
                                <li>Spotify URI: <a id="uri" href="#"></a></li>
                                <li>Link: <a id="url" href="#"></a></li>
                                <li>Profile Image: <span id="imgUrl"></span></li>
                            </ul>
                        </section>


                    </h2>
                </div>
            </div>
        }/>
    )
}