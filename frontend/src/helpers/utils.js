import jwt_decode from "jwt-decode";

function isLoggedIn() {
    const user = JSON.parse(localStorage.getItem('user'))
    return (user && user.data) ? true : false
}

function getUserId() {
    const user = JSON.parse(localStorage.getItem('user'))
    return jwt_decode(user.data).id
}

export {
    isLoggedIn, getUserId
}
