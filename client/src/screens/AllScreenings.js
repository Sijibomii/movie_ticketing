import React,{ useState, useEffect} from 'react'
import { getScreenings } from '../services/ScreeningService'
const AllScreenings = () => {
  const [screenings, setScreenings]=useState([])
  useEffect(()  => {
    const loadScreenings = async () => {
      const { response, isError } = await getScreenings();
      if (isError) {
        setScreenings([]);
      } else {
        console.log(response.data)
        setScreenings(response.data);
      }
    }
    loadScreenings();
  }, [])
  return (
    <>
    <div className="all__screenings">
      <div className="screenings__table">
          <table id="screenings">
          <tr>
        <th>Movie</th>
        <th className="d-sm-none">Venue</th>
        <th>Date</th>
        <th className="d-sm-none">Time</th>
        <th ></th>
      </tr>
      { screenings.map((screening)=>(
          <tr key={screening.id}>
            <td>{screening.movie.title}</td>
            <td className="d-sm-none">{screening.venue.name}</td>
            <td>{screening.date}</td>
            <td className="d-sm-none">{screening.time}</td>
            <td ><a href={`/screening/${screening.id}`}>BOOK A SEAT</a></td>
        </tr>
      ))}
          </table>
      </div>
    </div>
  
    </>
  )
}

export default AllScreenings
