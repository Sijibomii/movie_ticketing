import React, { useState, useEffect } from 'react'
import { Link } from "react-router-dom";
import { getMovies } from '../services/MovieService'
import { getScreenings } from '../services/ScreeningService'
const HomeScreen = () => {
  const [movies, setMovies]=useState([])
  const [screenings, setScreenings]=useState([])
  useEffect(()  => {
    const loadMovies = async () => {
      const { response, isError } = await getMovies();
      if (isError) {
        setMovies([]);
      } else {
        console.log(response.data)
        setMovies(response.data);
      }
    }
    loadMovies();
  }, [])
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
    <div className="hero">
      {/* <Header/> */}
      <div className="hero__container">
        <div className="hero__container__heading">
          <h2>Welcome to Our Cinemas!</h2>
          <h3>Book a ticket to watch tending<br/> movies and your favourite shows</h3>
        </div>
        <div className="hero__container__form">
          {/* <input type="text" placeholder="search for a movie here!"/> */}
          <Link to='/allscreenings'>BOOK A TICKET NOW</Link>

        </div>
      </div>
      
    </div>

    <section class="breweries" id="breweries">
      <h1>Top Trending Movies</h1>
    <ul>
      {movies.map((movie)=>(
         <li key={movie.id}>
          <figure>
          <img src={movie.image} className="cardd-img"/>
            <figcaption><h3>{movie.title}</h3></figcaption>
          </figure>
          <p>
            Made in the interiors of collapsing stars star stuff harvesting star light venture billions upon billions Drake Equation brain is the seed of intelligence?
          </p>
          <h4>{movie.duration} | {movie.rated}</h4>
          <h4>Released Aug 20</h4>
          <Link to={`/movie/${movie.id}`}>Book Ticket</Link>
       </li>
      ))}
    </ul>
  </section>
    
    {/* <Sliderr movies={movies}/> */}
    <div className="screenings__table">
      <div>
        <h2>Our Trending Screenings</h2>
        <Link to='/allscreenings'>SEE ALL SCREENINGS</Link>
      </div>
      
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
    {/* <Footer/> */} 
    </>
  )
}

export default HomeScreen
