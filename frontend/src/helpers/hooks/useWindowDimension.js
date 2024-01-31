// https://stackoverflow.com/questions/19014250/rerender-view-on-browser-resize-with-react

import { useEffect, useState } from 'react';

export default function useWindowDimension() {
    const [dimensions, setDimensions] = useState({ 
        height: window.innerHeight,
        width: window.innerWidth
    })

    useEffect(() => {
        function handleResize() {
            setDimensions({
                height: window.innerHeight,
                width: window.innerWidth
            })
        }
    
        window.addEventListener('resize', handleResize)
        return _ => {
            window.removeEventListener('resize', handleResize)
        }
    }, [])

    return dimensions
}