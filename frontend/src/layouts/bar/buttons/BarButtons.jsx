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
                    text_button={'My Friends'}
                />
                <Button
                    link_to={'/search-friends'}
                    icon={<i className="bi bi-people-fill"></i>}
                    text_button={'New Friends'}
                />
                {/* <Button 
                    link_to={'/vinyls'}
                    icon={<i className="bi bi-newspaper"></i>} 
                    text_button={'Search Vinyls'}
                /> */}
                <Button
                    link_to={'/playlists'}
                    icon={<i className="bi bi-newspaper"></i>}
                    text_button={'Playlists'}
                />
                <Button 
                    link_to={'/profile'}
                    icon={<i className="bi bi-robot"></i>} 
                    text_button={'External Apps'}
                />
                <Button
                    link_to={'/recommendation'}
                    icon={<i className="bi bi-people-fill"></i>}
                    text_button={'Recommendation'}
                />
        </div>
    )
}