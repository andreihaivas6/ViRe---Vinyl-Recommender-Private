import '../assets/styles/home.css'
import '../assets/styles/background.css'

import Bar from '../layouts/bar/Bar'
import Footer from '../layouts/footer/Footer'

import useWindowDimension from "../helpers/hooks/useWindowDimension";
import { WIDTH_FOR_RESPONSIVENESS, WIDTH_SIDEBAR } from "../config/config";

export default function PositionedPage({page}) {
    const dimension = useWindowDimension();
    let left_position = dimension.width > WIDTH_FOR_RESPONSIVENESS ? WIDTH_SIDEBAR : 0

    return (
        <div className="bg-light my_bg_class" >
            <Bar/>
            <div className="my-container" style={{
                position: "relative", 
                left: left_position, 
                width: dimension.width - left_position - 20, 
                minHeight: dimension.width >= WIDTH_FOR_RESPONSIVENESS ? "70.8vh" : "72.8vh",
                padding: 20,
            }}>
                <div style={{padding: 20}}>{page}</div>
                
            </div>
            <div style={{
                position: "relative", 
                left: left_position, 
                width: dimension.width - left_position,
                paddingBottom: 10
            }}>
                <div className="user-motivation text-center text-light">
                    <div className="text-area">
                        <strong className="d-block">
                            Vinyls are back!
                        </strong>
                        Receive Music Recommendations with our Application.
                    </div>
                </div>
            </div>
            <Footer/>
        </div>
    )
}