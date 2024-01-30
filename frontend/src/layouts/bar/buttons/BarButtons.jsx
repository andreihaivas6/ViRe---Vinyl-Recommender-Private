import Button from "./Button"

export default function BarButtons() {
    return (
        <div>

                <Button 
                    link_to={'/preferences'}
                    icon={<i className="bi bi-robot"></i>} 
                    text_button={'Home'}
                />
                <Button 
                    link_to={'/friends'}
                    icon={<i className="bi bi-people-fill"></i>} 
                    text_button={'Friends'}
                />
                <Button
                    link_to={'/search-friends'}
                    icon={<i className="bi bi-people-fill"></i>}
                    text_button={'Search Friends'}
                />
                <Button
                    link_to={'/recommendation'}
                    icon={<i className="bi bi-people-fill"></i>}
                    text_button={'Recommendation'}
                />
                <Button 
                    link_to={'/vinyls'}
                    icon={<i className="bi bi-newspaper"></i>} 
                    text_button={'Search Vinyls'}
                />
                <Button
                    link_to={'/playlists'}
                    icon={<i className="bi bi-newspaper"></i>}
                    text_button={'Playlists'}
                />
        </div>
    )
}