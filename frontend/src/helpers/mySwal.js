// https://sweetalert2.github.io/
// Modale
// https://code.tutsplus.com/tutorials/creating-pretty-popup-messages-using-sweetalert2--cms-30662

import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

const MySwal = withReactContent(Swal)

const icons = {
    success: 'success',
    info: 'info',
    error: 'error',
    question: 'question'
}

function swal({
    msg, 
    icon, 
    title=null, 
    showConfirmButton=false, 
    timer=2000
}) {
    if (showConfirmButton) {
        timer = null
    }

    MySwal.fire({
        text: msg,
        icon: icon,
        title: title,
        showConfirmButton: showConfirmButton,
        timer: timer,
    })
}

function notification(msg) {
    MySwal.mixin({
        toast: true,
        icon: 'success',
        title: msg,
        position: 'bottom-right',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', MySwal.stopTimer)
            toast.addEventListener('mouseleave', MySwal.resumeTimer)
        },
        background: 'black',
        color: 'white',
    }).fire()
}

function are_you_sure(msg, func) {
    MySwal.fire({
        title: 'Are you sure?',
        text: msg,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes!'
      }).then((result) => {
            if (result.isConfirmed) {
                func()
            }
      })
}


export {
    swal, icons, notification, are_you_sure,
}
