import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import Spinner from "../components/Spinner";


export default function Vinyl() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    // let vinyl = localStorage.getItem('vinyl')
    let vinyl = JSON.parse(localStorage.getItem('vinyl'))
    // has fields
    // title, artist, genre, date, imageURL

    return (
        <PositionedPage page={
            // <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25, padding: 20}}>
                <div className="text-center">
                    {/* <h2>Vinyl</h2> */}
                    {/* center div below */}
                    <div className="d-flex justify-content-center">
                        <div className="card " style={{width: '20rem'}}>
                            <img src={vinyl.imageUrl} className="card-img-top" alt="..."/>
                            <div className="card-body">
                                <h5 className="card-title">{vinyl.title}</h5>
                                <p className="card-text">{vinyl.artist}</p>
                                <p className="card-text">{vinyl.genre}</p>
                                <p className="card-text">{vinyl.date}</p>
                            </div>
                        </div>
                    </div>
                </div>
            // </div>
        } />
    )
}