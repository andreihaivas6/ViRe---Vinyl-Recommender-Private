import {Route, Routes, BrowserRouter} from 'react-router-dom'

import Home from './pages/Home';

import Demo from './pages/Demo';

import Login from './pages/user/Login';
import ConfirmationLogin from './pages/user/ConfirmationLogin';
import Register from './pages/user/Register';
import ForgotPassword from './pages/user/ForgotPassword';
import ResetPassword from './pages/user/ResetPassword';
import ConfirmationEmail from './pages/user/ConfirmationEmail'
import ResendConfirmationEmail from './pages/user/ResendConfirmationEmail';

import PrivateRoute from './helpers/routes/PrivateRoute';
import ProtectedRoute from './helpers/routes/ProtectedRoute';
import NotFoundPage from './pages/NotFoundPage';
import Preferences from "./pages/Preferences";
import Friends from "./pages/MyFriends";
import Recommendations from "./pages/Recommendations";
import Vinyls from "./pages/Vinyls";
import SearchFriends from "./pages/SearchFriends";
import Playlists from "./pages/Playlists";

export default function App() {  
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<ProtectedRoute><Home/></ProtectedRoute>}></Route>
                <Route path='/home' index element={<ProtectedRoute><Home/></ProtectedRoute>}></Route>
                
                {/* add Private Route for Demo */}
                <Route path='/demo' element={<PrivateRoute><Demo/></PrivateRoute>}></Route>
                <Route path='/preferences' element={<PrivateRoute><Preferences/></PrivateRoute>}></Route>
                <Route path='/friends' element={<PrivateRoute><Friends/></PrivateRoute>}></Route>
                <Route path='/search-friends' element={<PrivateRoute><SearchFriends/></PrivateRoute>}></Route>

                <Route path='/recommendation' element={<PrivateRoute><Recommendations/></PrivateRoute>}></Route>
                <Route path='/vinyls' element={<PrivateRoute><Vinyls/></PrivateRoute>}></Route>
                <Route path='/playlists' element={<PrivateRoute><Playlists/></PrivateRoute>}></Route>

                {/* <Route path='/profile' element={<PrivateRoute><Profile/></PrivateRoute>}></Route> */}

                <Route path='/login' element={<ProtectedRoute><Login/></ProtectedRoute>}></Route>
                <Route path='/confirmation_login' element={<ProtectedRoute><ConfirmationLogin/></ProtectedRoute>}></Route>
                <Route path='/register' element={<ProtectedRoute><Register/></ProtectedRoute>}></Route>
                <Route path='/forgot_password' element={<ProtectedRoute><ForgotPassword/></ProtectedRoute>}></Route>
                <Route path='/reset_password' element={<ProtectedRoute><ResetPassword/></ProtectedRoute>}></Route>
                <Route path='/confirmation_email' element={<ProtectedRoute><ConfirmationEmail/></ProtectedRoute>}></Route>
                <Route path='/resend_confirmation_email' element={<ProtectedRoute><ResendConfirmationEmail/></ProtectedRoute>}></Route>

                <Route path="*" element={<NotFoundPage/>} />
            </Routes>
        </BrowserRouter>
    )
}
