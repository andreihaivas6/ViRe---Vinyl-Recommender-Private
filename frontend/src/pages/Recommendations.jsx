import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import Spinner from "../components/Spinner";
import {Button} from "react-bootstrap";


export default function Recommendations() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    return (
        <PositionedPage page={
            <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25}}>
                <div className="text-center">
                    <h1 className="mx-auto my-0 text-uppercase text-dark pt-5">Demo</h1>
                    <p className="text-dark mx-auto mt-2 mb-5 pt-5">
                        This is a recommendation page.
                    </p>
                    <Button variant="primary" href="/recommendations"> Get Recommendations</Button>{' '}
                </div>
            </div>
        } />
    )
}