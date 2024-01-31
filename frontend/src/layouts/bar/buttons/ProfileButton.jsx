export default function ProfileButton() {
    const text_button = 'Hello, ' + localStorage.getItem('username') + '!'
    
    return (
        <div style={{padding: 12}} >
            <div> 
                {<i className="bi bi-person-circle"></i>}
                <span className="ms-2">{text_button}</span> 
            </div>
        </div>
    )
}
