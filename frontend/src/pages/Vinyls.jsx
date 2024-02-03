import PositionedPage from "./PositionedPage";
import useWindowDimension from "../helpers/hooks/useWindowDimension";
import Spinner from "../components/Spinner";


export default function Vinyls() {
    let size = useWindowDimension();
    const transparency = 0.7; // Adjust this value as needed

    return (
        <PositionedPage page={
            <div style={{backgroundColor: `rgba(255, 255, 255, ${transparency})`, borderRadius:25, padding: 20}}>
                <div className="text-center">
                    <h1 className="mx-auto my-0 text-uppercase text-dark pt-5">Demo</h1>
                    <h2 className="text-dark mx-auto mt-2 mb-5 pt-5">
                        This is a demo page.
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Deleniti dignissimos excepturi fugit id illum laboriosam laborum libero molestias, natus repudiandae rerum, suscipit tempora voluptatum! Ab, blanditiis cum dolores earum eligendi eos excepturi impedit, ipsa ipsum minus neque officia perspiciatis quae sapiente temporibus? Ad amet cumque dicta illo incidunt laudantium odio quam, repellat soluta vel. Accusamus aut, cupiditate debitis deleniti ea est eveniet ex fugiat fugit illum impedit minima non numquam possimus quam qui quia rem saepe, sed vero? Consequuntur deleniti earum harum minima quia rem vel! A at commodi dolor dolore earum, ex expedita id laborum nemo officia soluta voluptate!
                    </h2>
                </div>
            </div>
        } />
    )
}