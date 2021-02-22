import React,{ useEffect,useState } from 'react'
import { getDownloadTicket, getSeatsBooked } from '../services/ScreeningService'
import { Link } from 'react-router-dom';
import { getUser } from '../services/AuthService'
const DashboardScreen = ({ isLoggedIn, history  }) => {
  const[seats, setSeats]=useState([])
  const [user,setUser]=useState('')
  useEffect(() => {
   setUser(getUser())
  }, [])
  useEffect(()  => {
    const loadSeats = async () => {
      if(!isLoggedIn){
        history.push('/sign-in')
      }
      const { response, isError } = await getSeatsBooked();
      if (isError) {
        setSeats([]);
      } else {
        console.log(response.data)
        setSeats(response.data);
      }
    }
    loadSeats();
  }, [isLoggedIn])
  return (
    <div className="dashboard">
      <div className="dashboard__container">
        { isLoggedIn && user ? (
          <h1>Hello {user.username}!</h1>
        ):
        <>
        </>
        }
        
        <div className="dashboard__container__table">
        <table id="screenings">
          <tr>
            <th>Ticket ID</th>
            <th>Status</th>
            <th>Movie</th>
            <th>screening date/ time</th>
            <th></th>
          </tr>
          { seats.length !=0 ? (
            <>
            {seats.map((ticket)=>(
              <tr>
              <td>{ticket.id}</td>
              <td>{ticket.seat.status}</td>
              <td>{ticket.screening.movie.title}</td>
              <td>{ticket.screening.date}/{ticket.screening.time}</td>
              <td>
                <span>
                  <Link onClick={()=>{
                    return getDownloadTicket(ticket.id)
                  }}>Download Ticket</Link>
                  <i class="fas fa-trash fa-2x"></i>
                </span>
              </td>
            </tr>
            ))}
            </>
          ): (
            <>
            <h3>You have no tickets yet!</h3>
            </>
          )}
          
    </table>
        </div>
      </div>
    </div>
  )
}

export default DashboardScreen
