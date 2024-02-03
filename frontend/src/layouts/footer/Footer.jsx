// https://mdbootstrap.com/docs/standard/navigation/footer/

import useWindowDimension from "../../helpers/hooks/useWindowDimension"
import { WIDTH_FOR_RESPONSIVENESS, WIDTH_SIDEBAR } from "../../config/config";

export default function Footer() {
    const dimension = useWindowDimension();
    let left_position = dimension.width > WIDTH_FOR_RESPONSIVENESS ? WIDTH_SIDEBAR : 0
    
    return (
        <footer className="myFooter bg-dark text-center text-white" style={{
            position: "relative",
            left: left_position,
            bottom:0,
            // paddingBottom: 0,
            width: dimension.width - left_position - 20
        }}>
                <div className="container p-2 pb-0">
                    <section >
                    <a className="btn-rounded m-2" href="https://www.facebook.com/andrei.haivas/" role="button" target="_blank"><i className="bi bi-facebook fa-2x"></i></a>
                    <a className="btn-rounded m-3" href="https://twitter.com/DHaivas" role="button" target="_blank"><i className="bi bi-twitter fa-2x" /></a>
                    <a className="btn-rounded m-2" href="https://t.me/+AEha6Oht--41MmJk/" role="button" target="_blank"><i className="bi bi-telegram fa-3x" /></a>
                    <a className="btn-rounded m-3" href="https://www.linkedin.com/in/daniel-haivas/" role="button" target="_blank"><i className="bi bi-linkedin fa-2x" /></a>
                    <a className="btn-rounded m-2" href="https://github.com/andreihaivas6" role="button" target="_blank"><i className="bi bi-github fa-2x" /></a>
                    </section>
                </div>
                {/*<div className="text-center p-2 pb-3" style={{backgroundColor: 'rgba(0, 0, 0, 0.2)',}}>*/}
                {/*    © 2022 Copyright: */}
                {/*    <a className="text-white" style={{ padding:10}}>Haivas Daniel-Andrei</a>*/}
                {/*</div>*/}
        </footer>
    )
}