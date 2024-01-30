import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import '../assets/styles/preferences.css';
import {Button, Form} from "react-bootstrap";


export default function Preferences() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    return (
        <PositionedPage page={
            <div className="preferences-container" style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25}}>
                <div className="text-center">
                    {/*<p className="mx-auto my-0 text-dark pt-5">My music preferences</p>*/}
                    <div className="preferences" style={{width: '70%', margin: 'auto'}}>
                        <Form>
                            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                                <Form.Label> Enter your music preferences:</Form.Label>
                                <Form.Control placeholder="I like rock and roll"/>
                            </Form.Group>
                            <Button variant="secondary" type="submit">
                                Submit
                            </Button>
                        </Form>
                    </div>
                </div>
            </div>
        }/>
    )
}