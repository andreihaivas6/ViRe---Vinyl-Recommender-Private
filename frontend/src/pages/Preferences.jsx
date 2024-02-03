import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import '../assets/styles/preferences.css';
import {Button, Form} from "react-bootstrap";


export default function Preferences() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    const handleSentPreference = () => {
        let text = document.getElementById('text').value
        console.log(text)
    }

    return (
        <PositionedPage page={
            <div className="preferences-container" style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25}}>
                <div className="text-center">
                    {/*<p className="mx-auto my-0 text-dark pt-5">My music preferences</p>*/}
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
                </div>
            </div>
        }/>
    )
}