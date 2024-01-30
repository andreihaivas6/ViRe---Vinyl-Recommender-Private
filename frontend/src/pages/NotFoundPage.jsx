// https://bootsnipp.com/snippets/VgBP3

export default function NotFoundPage() {
    return (
        <div className="page-wrap d-flex flex-row align-items-center" style={{minHeight: "100vh"}}>
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-md-12 text-center">
                        <span className="display-1 d-block">404</span>
                        <div className="mb-4 lead">The page you are looking for was not found.</div>
                        <a href="/bots" className="btn btn-primary btn-lg">
                            <span className="glyphicon glyphicon-home">
                                Take Me Home 
                            </span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    )
}
