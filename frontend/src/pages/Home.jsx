// https://startbootstrap.com/previews/grayscale
import { Link } from 'react-router-dom'
import '../assets/styles/home.css'

export default function Home() {
    return (
        <header className="my_class">
            <div className="container px-4 px-lg-5 d-flex h-100 align-items-center justify-content-center ">
                <div className="d-flex justify-content-center">
                    <div className="text-center">
                        <h1 className="mx-auto my-0 text-uppercase text-white pt-5">Vinyl Recommendation</h1>
                        <h2 className="text-white-50 mx-auto mt-2 mb-5 pt-5">
                           Vinyl Recommendation is a web application that recommends vinyls to users based on their music taste.
                        </h2>
                        
                        <Link to='/login'>
                            <button className="btn btn-default " style={{fontSize:16, borderRadius:20}}>
                                Login
                            </button>
                        </Link>
                        <Link to='/register'>
                            <button className="btn btn-dark" style={{fontSize:16, borderRadius:20}}>
                                Register
                            </button>
                        </Link>
                        
                        <h2 className="text-white-50 mx-auto mt-2 mb-5 pt-5">Outperform the Market</h2>
                    </div>
                </div>
            </div>
        </header>
        
    )
}